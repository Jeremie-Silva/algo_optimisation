# ----------------------------------------------------------------------------------------
# https://github.com/Jeremie-Silva/algo_optimisation/blob/main/README.md
# ----------------------------------------------------------------------------------------

import csv
import argparse
import time
from itertools import combinations
from pydantic import BaseModel, model_validator


parser = argparse.ArgumentParser()
parser.add_argument("dataset_path", type=str, help="Type the path to your csv dataset")
args = parser.parse_args()


BUDGET: float = 500
DATASET_PATH: str = args.dataset_path


class Action(BaseModel):
    name: str
    price: float
    rent: float
    benefits: float = None

    @model_validator(mode='after')
    def calculate_benefits(self) -> None:
        """Calculate the benefits of the action after the model is initialized.
        Benefits are calculated by multiplying the price and rent percentage,
        and assigning the result to the benefits attribute.
        Complexity: O(1)
        """
        self.benefits = round(self.price * (self.rent / 100), 2)


class Scenario(BaseModel):
    budget: int = BUDGET
    actions: list
    cumulative_benefits: float = 0.0
    budget_remaining: float = 0.0

    def calculate_cumulative_benefits(self) -> None:
        """Calculates the cumulative benefits of all actions in the scenario.
        Complexity: O(BUDGET)
        """
        self.cumulative_benefits = round(sum([i.benefits for i in self.actions]), 2)

    def calculate_budget_remaining(self) -> None:
        """Calculates the remaining budget based on the actions in the scenario.
        Complexity: O(BUDGET)
        """
        self.budget_remaining = round(self.budget - sum([i.price for i in self.actions]), 2)

    def append_action_if_possible(self, action: Action) -> bool:
        """Appends an action to the scenario if it fits within the remaining budget.
        Complexity: O(1)

        Params:
            action: Action object to be added to the scenario.
        Returns:
            True if action was added, False otherwise.
        """
        if action.price <= self.budget_remaining and action not in self.actions:
            self.actions.append(action)
            return True
        else:
            return False

    def __str__(self):
        return f"Total benefits : {self.cumulative_benefits}€ \n" \
               f"Total coast : {self.budget - self.budget_remaining}€ \n" \
               f"Number of actions : {len(self.actions)} \n" \
               f"Actions name : {[i.name for i in self.actions]}"


def load_dataset(dataset_path: str) -> list[list[str]]:
    """Loads a dataset from a CSV file and returns it as a list of lists.
    Complexity: O(n)

    Params:
        dataset_path: Path to the CSV file.
    Returns:
        List of lists containing the dataset.
    """
    with open(dataset_path, "r") as file:
        unprocessed_dataset = [i for i in csv.reader(file)]
    return unprocessed_dataset[1:]


def format_dataset(data: list[list[str]]) -> list[Action]:
    """Formats the raw dataset into a list of Action objects.
    Complexity: O(n)

    Params:
        data: List of lists containing the raw dataset.
    Returns:
        List of Action objects.
    """
    return [Action(name=i[0], price=i[1], rent=i[2]) for i in data]


def clean_dataset(dataset: list[Action]) -> list[Action]:
    """Cleans the dataset by removing actions
    with non-positive benefits or non-positive prices.
    Complexity: O(n)

    Params:
        dataset: List of Action objects.
    Returns:
        Cleaned list of Action objects.
    """
    return [action for action in dataset if action.benefits > 0 and action.price > 0]


def calculates_best_scenario(dataset: list[Action]) -> Scenario:
    """Generates lists of combinations of different lengths,
    creates scenarios with these lists, returns the best scenario.
    Complexity: O(n^2 * 2^n)

    Params:
        dataset: List of Action objects.
    Returns:
        Scenario object.
    """
    best_scenario = Scenario(actions=[])
    for i in range(len(dataset)):
        combinations_increasing_length: list = list(combinations(dataset, i+1))

        for combination in combinations_increasing_length:
            new_scenario = Scenario(actions=[])
            for action in combination:
                new_scenario.append_action_if_possible(action)
                new_scenario.calculate_budget_remaining()

            new_scenario.calculate_cumulative_benefits()
            if new_scenario.cumulative_benefits > best_scenario.cumulative_benefits:
                best_scenario = new_scenario
    return best_scenario


def show_result(result: Scenario) -> None:
    """Displays the best result.
    Complexity: O(1)

    Params:
        result: Scenario object.
    """
    print("-------------------------------------------------------------------------")
    print(result)
    print("-------------------------------------------------------------------------")


if __name__ == "__main__":
    start_time = time.time()
    unprocessed_dataset: list[list[str]] = load_dataset(DATASET_PATH)  # O(n)
    dataset: list[Action] = format_dataset(unprocessed_dataset)  # O(n)
    dataset_clean: list[Action] = clean_dataset(dataset)  # O(n)
    result: Scenario = calculates_best_scenario(dataset_clean)  # O(n^2 * 2^n)
    show_result(result)  # O(1)
    end_time = time.time()
    print(f"Execution time: {end_time-start_time:.2f} seconds")
