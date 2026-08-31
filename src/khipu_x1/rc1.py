"""RC1 behavior emulator.

HMAC is used only to exercise protocol/state behavior. Production RC1 should use
secure-element-backed keys or public-key verification and protected monotonic
state. This module must never be represented as production hardware security.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from dataclasses import dataclass
from typing import Any, Mapping

from .kids import canonical_json_bytes
from .receipt import ReceiptChain


class RC1Rejected(PermissionError):
    pass


@dataclass(frozen=True)
class AuthorizationEnvelope:
    target_id: str
    channel: int
    requested_state: bool
    counter: int
    not_before: int
    expires_at: int
    policy_digest: str
    command_digest: str
    mac: str
    version: str = "rc1-emulator-0.1"

    def unsigned_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "target_id": self.target_id,
            "channel": self.channel,
            "requested_state": self.requested_state,
            "counter": self.counter,
            "not_before": self.not_before,
            "expires_at": self.expires_at,
            "policy_digest": self.policy_digest,
            "command_digest": self.command_digest,
        }

    def as_dict(self) -> dict[str, Any]:
        return {**self.unsigned_dict(), "mac": self.mac}


def sign_envelope(key: bytes, unsigned: Mapping[str, Any]) -> AuthorizationEnvelope:
    payload = dict(unsigned)
    payload.setdefault("version", "rc1-emulator-0.1")
    mac = hmac.new(key, canonical_json_bytes(payload), hashlib.sha256).hexdigest()
    return AuthorizationEnvelope(mac=mac, **payload)


class RC1Emulator:
    def __init__(self, target_id: str, key: bytes, channels: int = 4) -> None:
        if not target_id or not key:
            raise ValueError("target_id and key are required")
        self.target_id = target_id
        self._key = bytes(key)
        self.outputs = {index: False for index in range(channels)}
        self.last_counter = -1
        self.chain = ReceiptChain()

    def reset_to_safe_state(self, reason: str = "reset") -> None:
        for channel in self.outputs:
            self.outputs[channel] = False
        self.chain.append("rc1_safe_reset", {"target_id": self.target_id, "reason": reason})

    def authorize_and_apply(self, envelope: AuthorizationEnvelope, now: int | None = None) -> dict[str, Any]:
        timestamp = int(time.time()) if now is None else int(now)
        reason: str | None = None
        if envelope.version != "rc1-emulator-0.1":
            reason = "UNSUPPORTED_VERSION"
        elif envelope.target_id != self.target_id:
            reason = "WRONG_TARGET"
        elif envelope.channel not in self.outputs:
            reason = "INVALID_CHANNEL"
        elif envelope.counter <= self.last_counter:
            reason = "REPLAY_REJECTED"
        elif timestamp < envelope.not_before or timestamp > envelope.expires_at:
            reason = "EXPIRED_OR_NOT_YET_VALID"
        else:
            expected = hmac.new(
                self._key,
                canonical_json_bytes(envelope.unsigned_dict()),
                hashlib.sha256,
            ).hexdigest()
            if not hmac.compare_digest(expected, envelope.mac):
                reason = "AUTHENTICATION_FAILED"

        if reason is not None:
            event = self.chain.append(
                "rc1_rejected",
                {
                    "target_id": self.target_id,
                    "counter": envelope.counter,
                    "channel": envelope.channel,
                    "reason": reason,
                },
            )
            raise RC1Rejected(f"{reason}; receipt={event['digest']}")

        self.outputs[envelope.channel] = bool(envelope.requested_state)
        self.last_counter = envelope.counter
        return self.chain.append(
            "rc1_action_applied",
            {
                "target_id": self.target_id,
                "counter": envelope.counter,
                "channel": envelope.channel,
                "requested_state": envelope.requested_state,
                "policy_digest": envelope.policy_digest,
                "command_digest": envelope.command_digest,
                "execution_evidence_only": True,
                "outcome_verified": False,
            },
        )
