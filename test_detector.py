
import unittest

from detector import classify_event


class TestBankingEventDetection(unittest.TestCase):

    def test_normal_event_is_low_risk(self):
        event = {
            "failed_logins": 0,
            "amount": 2500,
            "country": "India",
        }

        risk, reason = classify_event(event)

        self.assertEqual(risk, "Low")
        self.assertEqual(reason, "No rule triggered")

    def test_repeated_failed_logins(self):
        event = {
            "failed_logins": 5,
            "amount": 0,
            "country": "India",
        }

        risk, reason = classify_event(event)

        self.assertEqual(risk, "Medium")
        self.assertIn("Repeated failed login attempts", reason)

    def test_high_value_transaction(self):
        event = {
            "failed_logins": 0,
            "amount": 100000,
            "country": "India",
        }

        risk, reason = classify_event(event)

        self.assertEqual(risk, "Medium")
        self.assertIn("High-value transaction", reason)

    def test_unknown_country(self):
        event = {
            "failed_logins": 0,
            "amount": 0,
            "country": "Unknown",
        }

        risk, reason = classify_event(event)

        self.assertEqual(risk, "Medium")
        self.assertIn("Unknown country", reason)

    def test_multiple_rules_produce_high_risk(self):
        event = {
            "failed_logins": 6,
            "amount": 125000,
            "country": "India",
        }

        risk, reason = classify_event(event)

        self.assertEqual(risk, "High")
        self.assertIn("Repeated failed login attempts", reason)
        self.assertIn("High-value transaction", reason)


if __name__ == "__main__":
    unittest.main()
