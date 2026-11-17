"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

from typing import Any

from lab8 import durability
from lab8.db import connect
from lab8.durability import InjectedCrash
from lab8.mock_llm import complete
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.tools import get_claim_view, tool_cost
from lab8.trace import Trace

SHAPE = "single"
MAX_STEPS = 8


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    budget = Budget()
    trace = Trace(make_run_id(SHAPE, claim_id, seed))
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at, budget=budget, trace=trace)
    except InjectedCrash:
        # The crash test expects the injected crash to reach the caller.
        raise
    except Exception as exc:  # run_claim must not raise; grader would record exception:<...>
        trace.add("error", {"type": type(exc).__name__})
        return _result(conn, claim_id, seed, "failed", 0, budget, trace, f"exception:{type(exc).__name__}")
    finally:
        conn.close()


def _run(
    conn,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
    budget: Budget,
    trace: Trace,
) -> RunResult:
    claim = get_claim_view(conn, claim_id)
    budget.add_tool(tool_cost())
    if not claim["found"]:
        trace.add("claim", {"found": False})
        return _result(conn, claim_id, seed, "failed", 0, budget, trace, "unknown_claim")

    principal_id = claim["principal_id"]
    order_id = claim["order_id"]
    # Trace only allowlisted fields. The ticket text is user data and stays out of the trace.
    trace.add("claim", {"found": True, "claim_id": claim_id, "order_id": order_id})

    if not order_id:
        trace.add("decision", {"status": "needs_info"})
        return _result(conn, claim_id, seed, "needs_info", 0, budget, trace, "missing_order_id")

    decide = _make_decide(
        budget,
        trace,
        seed=seed,
        claim_id=claim_id,
        order_id=order_id,
        principal_id=principal_id,
    )
    loop = run_react(
        conn,
        budget,
        observation={"claim": {"claim_id": claim_id, "order_id": order_id}},
        decide=decide,
        max_steps=MAX_STEPS,
    )
    if loop["stopped"] == "step_cap":
        return _result(conn, claim_id, seed, "failed", 0, budget, trace, "step_cap")

    final = loop["final"]
    if final["status"] == "escalated":
        trace.add("decision", {"status": "escalated", "reason": final.get("error_reason")})
        return _result(conn, claim_id, seed, "escalated", 0, budget, trace, final.get("error_reason"))
    if final["status"] != "quoted":
        return _result(conn, claim_id, seed, "failed", 0, budget, trace, final.get("error_reason"))

    # Money comes from the code quote, never from the model.
    quote = final["quote"]
    amount = int(quote["amount_vnd"])
    if amount <= 0:
        trace.add("decision", {"status": "denied", "reason": quote.get("reason")})
        return _result(conn, claim_id, seed, "denied", 0, budget, trace, quote.get("reason"))

    # Pass the FULL quote. The host subtracts earlier refunds on the same order.
    try:
        outcome = durability.issue_refund(conn, claim_id, amount, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    trace.add(
        "host",
        {"ok": outcome["ok"], "reason": outcome["reason"], "conflict": outcome["conflict"]},
    )
    if outcome["ok"]:
        return _result(conn, claim_id, seed, "resolved", amount, budget, trace, None)
    status = "failed" if outcome["conflict"] else "denied"
    return _result(conn, claim_id, seed, status, amount, budget, trace, outcome["reason"])


def _make_decide(
    budget: Budget,
    trace: Trace,
    *,
    seed: int,
    claim_id: str,
    order_id: str,
    principal_id: str,
):
    """Step policy for the single agent. Reads tools only; never sees the ticket text."""

    def decide(seen: dict[str, Any]) -> dict[str, Any]:
        last_tool = seen.get("last_tool")
        # One model call per step, so cost stays comparable with the other shapes.
        complete(budget, seed=seed, purpose="decide", prompt=f"{claim_id}|{last_tool}")

        if last_tool is None:
            return {
                "tool": "lookup_order",
                "args": {"order_id": order_id, "principal_id": principal_id},
            }

        result = seen["last_result"]
        if last_tool == "lookup_order":
            trace.add("lookup_order", result)
            if not result.get("visible"):
                return {"final": {"status": "escalated", "error_reason": result.get("reason")}}
            return {"tool": "compute_compensation", "args": {"order": result["order"]}}

        if last_tool == "compute_compensation":
            trace.add(
                "quote",
                {
                    "amount_vnd": result["amount_vnd"],
                    "reason": result["reason"],
                    "clause_ids": result["clause_ids"],
                    "parts": result["parts"],
                },
            )
            return {"final": {"status": "quoted", "quote": result}}

        return {"final": {"status": "failed", "error_reason": "unexpected_tool"}}

    return decide


def _result(
    conn,
    claim_id: str,
    seed: int,
    status: str,
    proposal_amount: int,
    budget: Budget,
    trace: Trace,
    error_reason: str | None,
) -> RunResult:
    return finish(
        conn,
        shape=SHAPE,
        claim_id=claim_id,
        seed=seed,
        status=status,
        proposal_amount=proposal_amount,
        budget=budget,
        trace=trace,
        error_reason=error_reason,
    )
