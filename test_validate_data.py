
import unittest
import pandas as pd

from validate_data import validate_events


class TestDatasetValidation(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame([
            {
                "event_id": "EVT-001",
                "account": "ACC-1001",
                "event_type": "login",
                "failed_logins": 0,
                "amount": 0,
                "country": "India",
                "status": "Success",
                "expected_label": "normal",
            }
        ])

    def test_valid_dataset(self):
        self.assertEqual(validate_events(self.data), [])

    def test_duplicate_event_ids(self):
        duplicate = pd.concat(
            [self.data, self.data],
            ignore_index=True,
        )
        self.assertIn(
            "Duplicate event IDs were found.",
            validate_events(duplicate),
        )

    def test_negative_amount(self):
        self.data.loc[0, "amount"] = -100
        self.assertIn(
            "Negative values found in amount.",
            validate_events(self.data),
        )

    def test_invalid_label(self):
        self.data.loc[0, "expected_label"] = "unknown_label"
        self.assertIn(
            "Unexpected reference label found.",
            validate_events(self.data),
        )

    def test_missing_column(self):
        incomplete = self.data.drop(columns=["country"])
        issues = validate_events(incomplete)

        self.assertTrue(
            any("Missing required columns" in issue for issue in issues)
        )


if __name__ == "__main__":
    unittest.main()
