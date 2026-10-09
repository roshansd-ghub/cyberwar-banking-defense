
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Cyberwar Banking Defense",
    page_icon="🛡️",
    layout="wide",
)

st.title("Cyberwar Banking Defense")
st.caption("Banking activity monitoring and security alert simulation")

# Fictional events created for testing the detection rules.
events = [
    {
        "event_id": "EVT-001",
        "account": "ACC-1001",
        "event_type": "login",
        "failed_logins": 1,
        "amount": 0,
        "country": "India",
        "status": "Success",
    },
    {
        "event_id": "EVT-002",
        "account": "ACC-1002",
        "event_type": "login",
        "failed_logins": 6,
        "amount": 0,
        "country": "India",
        "status": "Failed",
    },
    {
        "event_id": "EVT-003",
        "account": "ACC-1003",
        "event_type": "transaction",
        "failed_logins": 0,
        "amount": 125000,
        "country": "India",
        "status": "Completed",
    },
    {
        "event_id": "EVT-004",
        "account": "ACC-1004",
        "event_type": "transaction",
        "failed_logins": 0,
        "amount": 2500,
        "country": "India",
        "status": "Completed",
    },
    {
        "event_id": "EVT-005",
        "account": "ACC-1005",
        "event_type": "login",
        "failed_logins": 4,
        "amount": 0,
        "country": "Unknown",
        "status": "Failed",
    },
    {
        "event_id": "EVT-006",
        "account": "ACC-1006",
        "event_type": "transaction",
        "failed_logins": 0,
        "amount": 75000,
        "country": "India",
        "status": "Completed",
    },
    {
        "event_id": "EVT-007",
        "account": "ACC-1007",
        "event_type": "login",
        "failed_logins": 0,
        "amount": 0,
        "country": "India",
        "status": "Success",
    },
]

df = pd.DataFrame(events)

# Apply transparent rules to each simulated event.
def classify_event(row):
    reasons = []

    if row["failed_logins"] >= 5:
        reasons.append("Repeated failed login attempts")

    if row["amount"] >= 100000:
        reasons.append("High-value transaction")

    if row["country"] == "Unknown":
        reasons.append("Unknown country")

    if reasons:
        return pd.Series(
            ["High" if len(reasons) >= 2 else "Medium",
             "; ".join(reasons)]
        )

    return pd.Series(["Low", "No rule triggered"])


df[["risk_level", "alert_reason"]] = df.apply(
    classify_event, axis=1
)

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
