from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FeatureDefinition:
    name: str
    source_role: str
    operation: str
    periods: int | None = None
    window: int | None = None
    shift: int | None = None


def build_feature_registry(
    config: dict[str, Any],
) -> list[FeatureDefinition]:
    feature_store_config = config.get(
        "feature_store",
        {}
    )

    feature_config = feature_store_config.get(
        "features",
        {}
    )

    if not isinstance(
        feature_config,
        dict,
    ):
        raise ValueError(
            "feature_store.features must be a mapping."
        )

    registry: list[FeatureDefinition] = []

    for feature_name, definition in (
        feature_config.items()
    ):
        if not isinstance(
            definition,
            dict,
        ):
            raise ValueError(
                f"Feature '{feature_name}' "
                "must be configured as a mapping."
            )

        if not bool(
            definition.get(
                "enabled",
                True,
            )
        ):
            continue

        source_role = str(
            definition.get(
                "source_role",
                "",
            )
        ).strip()

        operation = str(
            definition.get(
                "operation",
                "",
            )
        ).strip()

        if not source_role:
            raise ValueError(
                f"Feature '{feature_name}' "
                "is missing source_role."
            )

        if not operation:
            raise ValueError(
                f"Feature '{feature_name}' "
                "is missing operation."
            )

        registry.append(
            FeatureDefinition(
                name=str(feature_name),
                source_role=source_role,
                operation=operation,
                periods=(
                    int(definition["periods"])
                    if definition.get(
                        "periods"
                    ) is not None
                    else None
                ),
                window=(
                    int(definition["window"])
                    if definition.get(
                        "window"
                    ) is not None
                    else None
                ),
                shift=(
                    int(definition["shift"])
                    if definition.get(
                        "shift"
                    ) is not None
                    else None
                ),
            )
        )

    if not registry:
        raise ValueError(
            "No enabled feature definitions "
            "were found."
        )

    return registry