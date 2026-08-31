from __future__ import annotations

import hashlib
import json
import time
import zipfile

import numpy as np
import pytest

from khipu_x1 import (
    Descriptor,
    KhipuPackageError,
    KhipuSimulator,
    KhipuValidationError,
    Opcode,
    RC1Emulator,
    RC1Rejected,
    ReceiptChain,
    build_package,
    lower_graph,
    sign_envelope,
    verify_package,
)


def d(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def test_descriptor_canonicalization_is_deterministic():
    descriptor = Descriptor(
        sequence=1,
        nonce=1,
        opcode=Opcode.NOP,
        model_digest=d("model"),
        policy_digest=d("policy"),
        attrs={"b": 2, "a": 1},
    )
    first = descriptor.canonical_bytes()
    second = descriptor.canonical_bytes()
    assert first == second
    assert json.loads(first)["attrs"] == {"a": 1, "b": 2}


def test_stream_replay_is_rejected():
    base = dict(opcode=Opcode.NOP, model_digest=d("m"), policy_digest=d("p"))
    sim = KhipuSimulator()
    with pytest.raises(KhipuValidationError):
        sim.execute([
            Descriptor(sequence=1, nonce=1, **base),
            Descriptor(sequence=1, nonce=2, **base),
        ])


def test_gemm_and_rmsnorm_match_reference():
    graph = {
        "model_digest": d("model"),
        "policy_digest": d("policy"),
        "ops": [
            {"op": "gemm_int8", "inputs": ["x", "w"], "output": "h", "attrs": {"scale": 0.25}},
            {"op": "rmsnorm", "inputs": ["h"], "output": "y", "attrs": {"eps": 1e-6}},
        ],
    }
    x = np.array([[1, -2, 3]], dtype=np.int8)
    w = np.array([[1, 2], [3, 4], [-1, 2]], dtype=np.int8)
    sim = KhipuSimulator()
    sim.register_buffer("x", x)
    sim.register_buffer("w", w)
    result = sim.execute(lower_graph(graph))
    h = (x.astype(np.int32) @ w.astype(np.int32)).astype(np.float32) * 0.25
    expected = h / np.sqrt(np.mean(np.square(h, dtype=np.float64), axis=-1, keepdims=True) + 1e-6)
    np.testing.assert_allclose(result.buffers["y"], expected.astype(np.float32), rtol=1e-6, atol=1e-6)
    assert result.chain.verify()[0]


def test_receipt_tamper_is_detected():
    chain = ReceiptChain()
    chain.append("x", {"value": 1})
    assert chain.verify()[0]
    chain.events[0]["payload"]["value"] = 2
    ok, index, reason = chain.verify()
    assert not ok and index == 0 and reason == "DIGEST_MISMATCH"


def test_rc1_replay_is_rejected():
    key = b"test-key"
    rc1 = RC1Emulator("unit", key)
    now = int(time.time())
    unsigned = {
        "target_id": "unit",
        "channel": 0,
        "requested_state": True,
        "counter": 1,
        "not_before": now - 1,
        "expires_at": now + 10,
        "policy_digest": d("policy"),
        "command_digest": d("command"),
    }
    envelope = sign_envelope(key, unsigned)
    rc1.authorize_and_apply(envelope, now=now)
    with pytest.raises(RC1Rejected, match="REPLAY_REJECTED"):
        rc1.authorize_and_apply(envelope, now=now)


def test_package_verification_and_duplicate_rejection(tmp_path):
    graph = {"model_digest": d("m"), "policy_digest": d("p"), "ops": [{"op": "nop"}]}
    path = build_package(tmp_path / "model.khipu", graph, {"w": np.ones((2, 2), dtype=np.int8)})
    assert verify_package(path)["verified"] is True
    with zipfile.ZipFile(path, "a") as archive:
        archive.writestr("graph.json", b"{}")
    with pytest.raises(KhipuPackageError, match="duplicate"):
        verify_package(path)
