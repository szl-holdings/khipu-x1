"""Minimal explicit graph-to-KIDS lowering.

This is an initial lowering reference, not a complete optimizing compiler.
"""

from __future__ import annotations

from typing import Any, Mapping

from .kids import Descriptor, KhipuValidationError, Opcode

_OP_MAP = {
    "nop": Opcode.NOP,
    "gemm_int8": Opcode.GEMM_INT8,
    "rmsnorm": Opcode.RMSNORM,
    "sha3_commit": Opcode.SHA3_COMMIT,
    "barrier": Opcode.BARRIER,
    "abort": Opcode.ABORT,
}


def lower_graph(graph: Mapping[str, Any]) -> list[Descriptor]:
    model_digest = str(graph.get("model_digest", ""))
    policy_digest = str(graph.get("policy_digest", ""))
    ops = graph.get("ops")
    if not isinstance(ops, list) or not ops:
        raise KhipuValidationError("graph.ops must be a non-empty list")

    descriptors: list[Descriptor] = []
    for index, op in enumerate(ops, start=1):
        if not isinstance(op, Mapping):
            raise KhipuValidationError(f"graph op {index} must be an object")
        logical_name = str(op.get("op", "")).lower()
        if logical_name not in _OP_MAP:
            raise KhipuValidationError(f"unsupported graph op: {logical_name}")
        descriptors.append(
            Descriptor(
                sequence=index,
                nonce=index,
                opcode=_OP_MAP[logical_name],
                model_digest=model_digest,
                policy_digest=policy_digest,
                inputs=tuple(str(item) for item in op.get("inputs", [])),
                output=None if op.get("output") is None else str(op["output"]),
                attrs=dict(op.get("attrs", {})),
                flags=tuple(str(item) for item in op.get("flags", [])),
            )
        )
    return descriptors
