"""Offline KHIPU-X1 + RC1 software-reference demonstration."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np

from khipu_x1 import (
    KhipuSimulator,
    RC1Emulator,
    build_package,
    lower_graph,
    sign_envelope,
    verify_package,
)


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def run_demo(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(11)
    x = rng.integers(-8, 8, size=(1, 4), dtype=np.int8)
    w = rng.integers(-8, 8, size=(4, 4), dtype=np.int8)

    graph = {
        "name": "tiny-khipu-reference",
        "model_digest": digest_text("tiny-khipu-reference-weights-v0.1"),
        "policy_digest": digest_text("observe-human-authorize-low-voltage-only"),
        "ops": [
            {"op": "gemm_int8", "inputs": ["x", "w"], "output": "hidden", "attrs": {"scale": 0.03125}},
            {"op": "rmsnorm", "inputs": ["hidden"], "output": "norm", "attrs": {"eps": 1e-6}},
            {"op": "sha3_commit", "inputs": ["norm"], "output": None, "attrs": {}},
        ],
    }

    package_path = build_package(
        output_dir / "tiny-reference.khipu",
        graph=graph,
        weights={"w": w},
        metadata={"hardware_status": "UNAVAILABLE", "purpose": "software-reference-demo"},
    )
    package_receipt = verify_package(package_path)

    simulator = KhipuSimulator()
    simulator.register_buffer("x", x)
    simulator.register_buffer("w", w)
    result = simulator.execute(lower_graph(graph))

    rc1_key = digest_text("DEMO-ONLY-NOT-A-PRODUCTION-KEY").encode("ascii")
    rc1 = RC1Emulator(target_id="beacon-zero", key=rc1_key, channels=2)
    now = int(time.time())
    unsigned = {
        "target_id": "beacon-zero",
        "channel": 0,
        "requested_state": True,
        "counter": 1,
        "not_before": now - 1,
        "expires_at": now + 60,
        "policy_digest": graph["policy_digest"],
        "command_digest": result.chain.head,
    }
    action_receipt = rc1.authorize_and_apply(sign_envelope(rc1_key, unsigned), now=now)

    # A real prototype must receive this from a physically independent input.
    # The software reference labels it simulated and never promotes it to a
    # hardware-observed outcome.
    simulated_witness = {
        "source": "SIMULATED_WITNESS_ONLY",
        "channel": 0,
        "observed_state": rc1.outputs[0],
        "outcome_verified": False,
        "reality_debt": "OPEN_UNTIL_PHYSICAL_WITNESS_EXISTS",
    }

    summary = {
        "program": "KHIPU-X1 software reference",
        "hardware_status": "UNAVAILABLE",
        "execution": result.summary(),
        "package": package_receipt,
        "rc1_action_receipt": action_receipt,
        "witness": simulated_witness,
    }
    (output_dir / "demo-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "execution-receipts.json").write_text(
        json.dumps(result.chain.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "rc1-receipts.json").write_text(
        json.dumps(rc1.chain.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="demo-output")
    args = parser.parse_args()
    print(json.dumps(run_demo(Path(args.out)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
