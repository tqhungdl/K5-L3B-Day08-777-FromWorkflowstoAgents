"""R2 ablation (report/team/research_card.md): reference swarm with ONE change.

The REFERENCE_WEAKNESS branch in lab8/shapes/swarm_reference.py only overrides
delay_days when parse_delay_days(ticket) returns a number. This variant runs the same
swarm code with that parser returning None, so delay_days always comes from the DB.
Topology, MockLLM calls (peer/parse/draft), tools, prices and evaluator are unchanged.
run_id uses "swarm_r2" so traces do not collide with the baseline.
swarm_reference.py itself is not edited. Not a graded shape.

python -m lab8.benchmark --shapes swarm,swarm_r2 \
    --extra-shape swarm_r2=experiments.r2_swarm_db_delay:run_claim \
    --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/ablation_r2.json
"""

from __future__ import annotations

from unittest import mock

from lab8.schemas import RunResult, make_run_id
from lab8.shapes import swarm_reference


def _run_id(shape: str, claim_id: str, seed: int) -> str:
    return make_run_id("swarm_r2" if shape == "swarm" else shape, claim_id, seed)


def run_claim(claim_id: str, *, seed: int, store_path: str, crash_at: str | None = None) -> RunResult:
    with (
        mock.patch.object(swarm_reference, "parse_delay_days", lambda _ticket: None),
        mock.patch.object(swarm_reference, "make_run_id", _run_id),
    ):
        return swarm_reference.run_claim(claim_id, seed=seed, store_path=store_path, crash_at=crash_at)
