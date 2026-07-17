"""Lightweight filesystem experiment tracking."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class ExperimentRecord:
    """Serializable experiment metadata."""

    experiment_id: str
    task_name: str
    model_name: str
    generated_at_utc: str
    parameters: dict[str, Any]
    metrics: dict[str, Any]
    artifact_path: str | None


def build_experiment_record(
    *,
    task_name: str,
    model_name: str,
    parameters: dict[str, Any] | None = None,
    metrics: dict[str, Any] | None = None,
    artifact_path: str | None = None,
) -> ExperimentRecord:
    """Build one immutable experiment record."""

    if not task_name.strip():
        raise ValueError(
            "task_name must not be empty."
        )

    if not model_name.strip():
        raise ValueError(
            "model_name must not be empty."
        )

    return ExperimentRecord(
        experiment_id=uuid4().hex,
        task_name=task_name,
        model_name=model_name,
        generated_at_utc=datetime.now(
            timezone.utc
        ).isoformat(),
        parameters=(
            parameters
            if parameters is not None
            else {}
        ),
        metrics=(
            metrics
            if metrics is not None
            else {}
        ),
        artifact_path=artifact_path,
    )


def write_experiment_record(
    *,
    record: ExperimentRecord,
    output_directory: Path,
) -> Path:
    """Persist an experiment record as JSON."""

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_directory
        / f"{record.experiment_id}.json"
    )

    output_path.write_text(
        json.dumps(
            asdict(
                record
            ),
            indent=2,
        ),
        encoding="utf-8",
    )

    return output_path