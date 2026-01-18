from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ieim.determinism.jcs import jcs_bytes
from ieim.raw_store import sha256_prefixed


@dataclass(frozen=True)
class JobKey:
    stage: str
    message_id: str
    config_sha256: str
    inputs_sha256: str


def build_inputs_sha256(*, inputs: dict[str, Any]) -> str:
    if not isinstance(inputs, dict):
        raise ValueError("inputs must be an object")
    return sha256_prefixed(jcs_bytes(inputs))


def build_job_id(*, stage: str, message_id: str, config_sha256: str, inputs_sha256: str) -> str:
    key = JobKey(
        stage=str(stage),
        message_id=str(message_id),
        config_sha256=str(config_sha256),
        inputs_sha256=str(inputs_sha256),
    )
    obj = {
        "config_sha256": key.config_sha256,
        "inputs_sha256": key.inputs_sha256,
        "message_id": key.message_id,
        "stage": key.stage,
    }
    return sha256_prefixed(jcs_bytes(obj))

