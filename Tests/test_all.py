from unittest import TestCase
from App.v3 import Action, Scenario


class AllTest(TestCase):
    def setUp(self):
        self.action_1 = Action(name="test name1", price=10.1, rent=25.6)
        self.action_2 = Action(name="test name2", price=64.80, rent=4.3)
        self.action_3 = Action(name="test name3", price=23.4, rent=12.58)

        self.scenario_1 = Scenario(
            budget=500,
            actions=[self.action_1, self.action_2, self.action_3]
        )

    def test_action_model(self):
        self.assertIsInstance(self.action_1, Action)
        self.assertIsInstance(self.action_2, Action)
        self.assertIsInstance(self.action_3, Action)
        self.assertEqual(self.action_1.benefits, 2.59)
        self.assertEqual(self.action_2.benefits, 2.79)
        self.assertEqual(self.action_3.benefits, 2.94)

    def test_scenario_model_calculate_cumulative_benefits(self):
        self.scenario_1.calculate_cumulative_benefits()
        self.assertEqual(self.scenario_1.cumulative_benefits, 8.32)

    def test_scenario_model_calculate_budget_remaining(self):
        self.scenario_1.calculate_budget_remaining()
        self.assertEqual(self.scenario_1.budget_remaining, 401.7)