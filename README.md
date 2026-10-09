
# Cyberwar Banking Defense

A small Python project for exploring banking cybersecurity
through simulated events, rule-based detection, and a
security monitoring dashboard.

## Project Overview

Cyberwar Banking Defense demonstrates how a basic defensive
monitoring system can identify events that deserve further
investigation.

The application processes fictional login and transaction
events, assigns risk levels using transparent rules, and
displays the results in a Streamlit dashboard.

## Features

- Simulated banking security events
- Rule-based risk classification
- High, medium, and low risk levels
- Event type and risk filters
- Dashboard metrics and a bar chart
- CSV export for further investigation
- Suggested defensive actions

## Detection Rules

| Condition | Risk level | Reason |
|---|---|---|
| 5 or more failed logins | Medium | Repeated authentication failures |
| Transaction amount of 100000 or more | Medium | High-value transaction |
| Country recorded as Unknown | Medium | Location requires verification |
| Two or more conditions match | High | Multiple risk indicators |

These are demonstration thresholds, not validated banking
fraud rules. A flagged event is not proof of an attack.

## Technologies

- Python
- Pandas
- Streamlit

## Requirements

Install Python 3 and a terminal that can run Python commands.

## Run Locally

Create and activate a virtual environment, then install
the required packages.

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r requirements.txt
    python -m streamlit run app.py

## Limitations

This version uses a small, fixed set of fictional events.
It does not connect to banking APIs, detect real-time attacks,
or verify whether transactions are fraudulent.

## Future Improvements

- Load events from a CSV file
- Add timestamps and event history
- Create unit tests for the detection rules
- Evaluate detection accuracy on a labelled synthetic dataset
- Add a more detailed incident investigation report

## Responsible Use

This project is for educational and defensive cybersecurity
learning. It uses synthetic data and is not intended for
production banking environments.
