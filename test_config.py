import json
import unittest
from pathlib import Path



class ConfigTests(unittest.TestCase):
    def test_monitoring_config_has_project_and_region(self):
        path = Path(__file__).resolve().parents[1] / "config" / "monitoring_config.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(config["project_name"], "OpsPulse")
        self.assertTrue(config["default_region"])

    def test_dashboard_json_is_valid(self):
        path = Path(__file__).resolve().parents[1] / "dashboards" / "opspulse_dashboard.json"
        dashboard = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("widgets", dashboard)
        self.assertGreater(len(dashboard["widgets"]), 0)

    def test_alarm_examples_json_is_valid(self):
        path = Path(__file__).resolve().parents[1] / "alarms" / "cloudwatch_alarms.json"
        alarms = json.loads(path.read_text(encoding="utf-8"))
        self.assertGreater(len(alarms["alarm_examples"]), 0)



if __name__ == "__main__":
    unittest.main()
