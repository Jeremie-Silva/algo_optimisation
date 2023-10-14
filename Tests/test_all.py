from unittest import TestCase
from App.optimized import Action, Scenario


class AllTests(TestCase):
    def setUp(self):
        self.action_1 = Action(name="test 1", price=10.1, rent=25.6)
        self.action_2 = Action(name="test 2", price=64.80, rent=4.3)
        self.action_3 = Action(name="test 3", price=23.4, rent=12.58)
        self.action_low_coast = Action(name="test 4", price=0.4, rent=2.34)

        self.scenario_1 = Scenario(
            budget=500,
            actions=[self.action_1, self.action_2, self.action_3]
        )

    # Action()

    def test_action_model(self):
        self.assertIsInstance(self.action_1, Action)
        self.assertIsInstance(self.action_2, Action)
        self.assertIsInstance(self.action_3, Action)

    # Action.calculate_benefits()

    def test_action_model_calculate_benefits(self):
        self.assertEqual(self.action_1.benefits, 2.59)
        self.assertEqual(self.action_2.benefits, 2.79)
        self.assertEqual(self.action_3.benefits, 2.94)

    # Scenario()

    def test_scenario_model(self):
        self.assertIsInstance(self.scenario_1, Scenario)

    # Scenario.calculate_cumulative_benefits()

    def test_scenario_model_calculate_cumulative_benefits(self):
        self.scenario_1.calculate_cumulative_benefits()
        self.assertEqual(self.scenario_1.cumulative_benefits, 8.32)

    # Scenario.calculate_budget_remaining()

    def test_scenario_model_calculate_budget_remaining(self):
        self.scenario_1.calculate_budget_remaining()
        self.assertEqual(self.scenario_1.budget_remaining, 401.7)

    # Scenario.append_action_if_possible()

    def test_scenario_model_append_action_if_possible(self):
        self.scenario_1.budget_remaining = 0.4
        self.assertTrue(
            self.scenario_1.append_action_if_possible(self.action_low_coast)
        )
        self.scenario_1.budget_remaining = 0
        self.assertFalse(
            self.scenario_1.append_action_if_possible(self.action_low_coast)
        )
