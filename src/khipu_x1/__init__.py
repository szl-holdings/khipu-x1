"""KHIPU-X1 software reference package."""

from .compiler import lower_graph
from .kids import Descriptor, KhipuValidationError, Opcode
from .package import KhipuPackageError, build_package, verify_package
from .rc1 import AuthorizationEnvelope, RC1Emulator, RC1Rejected, sign_envelope
from .receipt import ReceiptChain
from .simulator import ExecutionResult, KhipuExecutionError, KhipuSimulator, array_commitment

__all__ = [
    "AuthorizationEnvelope",
    "Descriptor",
    "ExecutionResult",
    "KhipuExecutionError",
    "KhipuPackageError",
    "KhipuSimulator",
    "KhipuValidationError",
    "Opcode",
    "RC1Emulator",
    "RC1Rejected",
    "ReceiptChain",
    "array_commitment",
    "build_package",
    "lower_graph",
    "sign_envelope",
    "verify_package",
]
