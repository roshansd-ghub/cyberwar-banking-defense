
import pandas as pd
import streamlit as st
from datetime import datetime
from detector import classify_event

st.set_page_config(
    page_title="Cyberwar Banking Defense",
    page_icon="🛡️",
    layout="wide",
)

st.title("Cyberwar Banking Defense")
st.caption("Banking activity monitoring and security alert simulation")

# Fictional events created for testing the detection rules.

from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "banking_events.csv"

df = pd.read_csv(DATA_FILE)
df[["risk_level", "alert_reason"]] = pd.DataFrame(
    df.apply(
        lambda row: classify_event(row),
        axis=1
    ).tolist(),
    index=df.index,
    columns=["risk_level", "alert_reason"],
)

# Evaluate the rules against the synthetic reference labels.
df["expected_label"] = (
    df["expected_label"].astype(str).str.strip().str.lower()
)

valid_labels = {"normal", "suspicious"}

if not set(df["expected_label"]).issubset(valid_labels):
    st.error("expected_label must contain only normal or suspicious.")
    st.stop()

df["actual_suspicious"] = df["expected_label"] == "suspicious"
df["predicted_suspicious"] = df["risk_level"] != "Low"

tp = int(
    (df["actual_suspicious"] & df["predicted_suspicious"]).sum()
)
fp = int(
    (~df["actual_suspicious"] & df["predicted_suspicious"]).sum()
)
fn = int(
    (df["actual_suspicious"] & ~df["predicted_suspicious"]).sum()
)
tn = int(
    (~df["actual_suspicious"] & ~df["predicted_suspicious"]).sum()
)

precision = tp / (tp + fp) if tp + fp else 0.0
recall = tp / (tp + fn) if tp + fn else 0.0
false_positive_rate = fp / (fp + tn) if fp + tn else 0.0

# Validate the columns required by the detection engine.
required_columns = {
    "event_id",
    "account",
    "event_type",
    "failed_logins",
    "amount",
    "country",
    "status",
    "expected_label",
}

missing_columns = required_columns.difference(df.columns)

if missing_columns:
    st.error(
        "Dataset is missing columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

df["failed_logins"] = pd.to_numeric(
    df["failed_logins"], errors="raise"
)
df["amount"] = pd.to_numeric(df["amount"], errors="raise")

st.sidebar.header("Investigation filters")

risk_options = st.sidebar.multiselect(
    "Risk level",
    ["High", "Medium", "Low"],
    default=["High", "Medium", "Low"],
)

type_options = st.sidebar.multiselect(
    "Event type",
    sorted(df["event_type"].unique()),
    default=sorted(df["event_type"].unique()),
)

filtered = df[
    df["risk_level"].isin(risk_options)
    & df["event_type"].isin(type_options)
]

high_count = int((df["risk_level"] == "High").sum())
medium_count = int((df["risk_level"] == "Medium").sum())
alert_count = int((df["risk_level"] != "Low").sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total events", len(df))
col2.metric("Alerts", alert_count)
col3.metric("High risk", high_count)
col4.metric("Medium risk", medium_count)

st.subheader("Detection performance")

m1, m2, m3 = st.columns(3)

m1.metric("Precision", f"{precision:.1%}")
m2.metric("Recall", f"{recall:.1%}")
m3.metric("False-positive rate", f"{false_positive_rate:.1%}")

st.caption(
    "Evaluation uses manually assigned synthetic labels. "
    "Results are illustrative and do not represent real-world "
    "banking fraud detection performance."
)

with st.expander("View evaluation counts"):
    st.write(f"True positives: {tp}")
    st.write(f"False positives: {fp}")
    st.write(f"False negatives: {fn}")
    st.write(f"True negatives: {tn}")

st.subheader("Security event overview")

chart_data = (
    df.groupby(["event_type", "risk_level"])
    .size()
    .unstack(fill_value=0)
)

st.bar_chart(chart_data)

st.subheader("Investigate events")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "Export filtered events as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="security_events.csv",
    mime="text/csv",
)

st.subheader("Recommended defensive actions")

st.markdown(
    """
    - **Repeated failed logins:** Review authentication logs,
      apply rate limiting, and investigate account access.
    - **High-value transactions:** Verify against the bank's
      authorized transaction limits and review for fraud.
    - **Unknown country:** Check trusted location and device
      signals before deciding whether to escalate.
    - **Low-risk events:** Continue routine monitoring.
    """
)

st.caption(
    "Demo environment | Synthetic data | "
    f"Dashboard generated {datetime.now().strftime('%Y-%m-%d %H:%M')}"
)
