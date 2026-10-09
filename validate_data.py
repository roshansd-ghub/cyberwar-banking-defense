
import pandas as pd


REQUIRED_COLUMNS = {
    "event_id",
    "account",
    "event_type",
    "failed_logins",
    "amount",
    "country",
    "status",
    "expected_label",
}

VALID_LABELS = {"normal", "suspicious"}
VALID_EVENT_TYPES = {"login", "transaction"}


def validate_events(df):
    """Return a list of data-quality problems."""

    issues = []

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        return [
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        ]

    if df.empty:
        issues.append("Dataset contains no events.")

    if df["event_id"].isna().any():
        issues.append("Some events have a missing event ID.")
    elif df["event_id"].duplicated().any():
        issues.append("Duplicate event IDs were found.")

    for column in ["account", "event_type", "country", "status",
                   "expected_label"]:
        if df[column].isna().any():
            issues.append(f"Missing values found in {column}.")

    for column in ["failed_logins", "amount"]:
        values = pd.to_numeric(df[column], errors="coerce")

        if values.isna().any():
            issues.append(f"Invalid numeric values in {column}.")
        elif (values < 0).any():
            issues.append(f"Negative values found in {column}.")

    if not df["event_type"].dropna().isin(
        VALID_EVENT_TYPES
    ).all():
        issues.append("Unexpected event type found.")

    labels = (
        df["expected_label"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
    )

    if not labels.isin(VALID_LABELS).all():
        issues.append("Unexpected reference label found.")

    return issues
