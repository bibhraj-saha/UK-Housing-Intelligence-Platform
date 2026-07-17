"""Filesystem-backed model registry."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_ALLOWED_STAGES = {
    "candidate",
    "staging",
    "production",
    "archived",
}


@dataclass(frozen=True)
class ModelRegistryEntry:
    """One registered model version."""

    task_name: str
    model_name: str
    version: int
    stage: str
    registered_at_utc: str
    artifact_path: str
    metrics: dict[str, Any]
    metadata: dict[str, Any]


def _load_registry(
    path: Path,
) -> dict[str, Any]:
    if not path.exists():
        return {
            "models": {},
        }

    loaded = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(
        loaded,
        dict,
    ):
        raise ValueError(
            "Model registry must contain "
            "a JSON mapping."
        )

    models = loaded.get(
        "models"
    )

    if not isinstance(
        models,
        dict,
    ):
        raise ValueError(
            "Model registry must contain "
            "a 'models' mapping."
        )

    return loaded


def register_model(
    *,
    registry_path: Path,
    task_name: str,
    model_name: str,
    artifact_path: str,
    metrics: dict[str, Any],
    stage: str = "candidate",
    metadata: dict[str, Any] | None = None,
) -> ModelRegistryEntry:
    """Register a new immutable model version."""

    if not task_name.strip():
        raise ValueError(
            "task_name must not be empty."
        )

    if not model_name.strip():
        raise ValueError(
            "model_name must not be empty."
        )

    if stage not in _ALLOWED_STAGES:
        raise ValueError(
            "Unknown model stage "
            f"'{stage}'."
        )

    registry = _load_registry(
        registry_path
    )

    models = registry[
        "models"
    ]

    task_versions = models.setdefault(
        task_name,
        [],
    )

    if not isinstance(
        task_versions,
        list,
    ):
        raise ValueError(
            f"Registry task '{task_name}' "
            "must contain a list."
        )

    version = (
        max(
            (
                int(
                    item["version"]
                )
                for item in task_versions
            ),
            default=0,
        )
        + 1
    )

    entry = ModelRegistryEntry(
        task_name=task_name,
        model_name=model_name,
        version=version,
        stage=stage,
        registered_at_utc=datetime.now(
            timezone.utc
        ).isoformat(),
        artifact_path=artifact_path,
        metrics=metrics,
        metadata=(
            metadata
            if metadata is not None
            else {}
        ),
    )

    task_versions.append(
        asdict(
            entry
        )
    )

    registry_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    registry_path.write_text(
        json.dumps(
            registry,
            indent=2,
        ),
        encoding="utf-8",
    )

    return entry