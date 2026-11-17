"""CP4: approval, trace safety, and crash recovery through the workflow."""

from pathlib import Path

import pytest

from lab8.db import connect
from lab8.durability import InjectedCrash
from lab8.shapes.workflow import run_claim
from tests.conftest import BY_ID


@pytest.mark.parametrize(
    "statement, params, reason",
    [
        ("UPDATE claims SET approval_id = ? WHERE claim_id = 'C-001'", (None,), "missing_approval"),
        ("UPDATE claims SET approval_id = ? WHERE claim_id = 'C-001'", ("A-002",), "approval_claim_mismatch"),
        ("UPDATE approvals SET status = ? WHERE approval_id = 'A-001'", ("revoked",), "approval_revoked"),
        ("UPDATE approvals SET expires_at = ? WHERE approval_id = 'A-001'", ("2000-01-01",), "approval_expired"),
    ],
    ids=["missing", "wrong-claim", "revoked", "expired"],
)
def test_invalid_approval_denies_refund(public_db, tmp_path, monkeypatch, statement, params, reason):
    monkeypatch.chdir(tmp_path)
    conn = connect(public_db)
    try:
        conn.execute(statement, params)
        conn.commit()
    finally:
        conn.close()

    result = run_claim("C-001", seed=11, store_path=str(public_db))

    assert result.status == "denied"
    assert result.error_reason == reason
    assert result.proposal_amount == 35000
    assert result.refund_effects == []
    assert result.committed_audit_count == 0
    conn = connect(public_db)
    try:
        denial = conn.execute(
            "SELECT details_json FROM audit_events WHERE claim_id = ? AND event_type = 'policy_denied'",
            ("C-001",),
        ).fetchone()
        assert denial is not None
        assert reason in denial["details_json"]
    finally:
        conn.close()


@pytest.mark.parametrize("point", ["before_effect", "after_effect_before_checkpoint", "after_checkpoint"])
def test_crash_then_repeated_resume_keeps_one_refund(public_db, tmp_path, monkeypatch, point):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(InjectedCrash):
        run_claim("C-001", seed=11, store_path=str(public_db), crash_at=point)

    for _ in range(2):
        result = run_claim("C-001", seed=11, store_path=str(public_db))
        assert result.status == "resolved"
        assert len(result.refund_effects) == 1
        assert result.refund_effects[0]["amount_vnd"] == 35000
        assert result.committed_audit_count == 1


@pytest.mark.parametrize("claim_id", ["C-001", "C-004", "C-005", "C-010"])
def test_trace_and_stdout_exclude_sensitive_data(public_db, tmp_path, monkeypatch, capsys, claim_id):
    monkeypatch.chdir(tmp_path)
    result = run_claim(claim_id, seed=11, store_path=str(public_db))
    captured = capsys.readouterr()
    # Include every side artifact matching the run id, as the grader does.
    trace_path = Path(result.trace_path)
    artifacts = "\n".join(
        path.read_text(encoding="utf-8")
        for path in trace_path.parent.glob(f"{result.run_id}*")
        if path.is_file()
    )
    output = artifacts + captured.out + captured.err + str(result.as_dict())
    assert trace_path.is_file()
    assert "CANARY_SECRET_" not in output
    assert BY_ID[claim_id]["ticket"] not in output
    for forbidden in BY_ID[claim_id]["expected"]["forbid_substrings"]:
        assert forbidden not in output
