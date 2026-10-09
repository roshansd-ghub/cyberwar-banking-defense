
def classify_event(row):
    """
    Classify a simulated banking event using simple rules.

    This function supports dictionaries and pandas Series.
    It does not determine whether fraud actually occurred.
    """
    reasons = []

    failed_logins = int(row.get("failed_logins", 0))
    amount = float(row.get("amount", 0))
    country = str(row.get("country", "")).strip()

    if failed_logins >= 5:
        reasons.append("Repeated failed login attempts")

    if amount >= 100000:
        reasons.append("High-value transaction")

    if country.lower() == "unknown":
        reasons.append("Unknown country")

    if len(reasons) >= 2:
        risk_level = "High"
    elif len(reasons) == 1:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return risk_level, (
        "; ".join(reasons) if reasons else "No rule triggered"
    )
