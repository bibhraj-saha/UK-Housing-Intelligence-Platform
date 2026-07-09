from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LeakageCheckResult:
    is_valid: bool
    approved_columns: list[str]
    rejected_columns: list[str]


def _normalise_column_name(
    column: str,
) -> str:
    return (
        str(column)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def validate_feature_columns(
    feature_columns: list[str],
    *,
    target_column: str | None = None,
    forbidden_name_tokens: list[str] | None = None,
    explicitly_forbidden_columns: list[str] | None = None,
) -> LeakageCheckResult:
    forbidden_tokens = [
        _normalise_column_name(token)
        for token in (
            forbidden_name_tokens
            if forbidden_name_tokens is not None
            else [
                "future",
                "target",
                "label",
                "prediction",
                "predicted",
            ]
        )
    ]

    forbidden_columns = {
        _normalise_column_name(column)
        for column in (
            explicitly_forbidden_columns
            if explicitly_forbidden_columns
            is not None
            else []
        )
    }

    if target_column is not None:
        forbidden_columns.add(
            _normalise_column_name(
                target_column
            )
        )

    approved: list[str] = []
    rejected: list[str] = []

    for column in feature_columns:
        normalised = _normalise_column_name(
            column
        )

        has_forbidden_token = any(
            token in normalised
            for token in forbidden_tokens
        )

        is_explicitly_forbidden = (
            normalised in forbidden_columns
        )

        if (
            has_forbidden_token
            or is_explicitly_forbidden
        ):
            rejected.append(
                str(column)
            )
        else:
            approved.append(
                str(column)
            )

    return LeakageCheckResult(
        is_valid=not rejected,
        approved_columns=sorted(
            approved
        ),
        rejected_columns=sorted(
            rejected
        ),
    )