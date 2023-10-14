from typing import List

from pydantic import BaseModel, model_validator
import csv


BUDGET: float = 500
DATASET_PATH: str = "../Data/dataset_1.csv"


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
        """
        self.benefits = round(self.price*(self.rent/100), 2)


class Scenario(BaseModel):
    budget: int = BUDGET
    actions: list
    cumulative_benefits: float = None
    budget_remaining: float = None

    def calculate_cumulative_benefits(self) -> None:
        """Calculates the cumulative benefits of all actions in the scenario."""
        self.cumulative_benefits = round(sum([i.benefits for i in self.actions]), 2)

    def calculate_budget_remaining(self) -> None:
        """Calculates the remaining budget based on the actions in the scenario."""
        self.budget_remaining = round(self.budget - sum([i.price for i in self.actions]), 2)

    def append_action_if_possible(self, action: Action) -> bool:
        """Appends an action to the scenario if it fits within the remaining budget.

        :param action: Action object to be added to the scenario.
        :return: True if action was added, False otherwise.
        """
        if action.price <= self.budget_remaining:
            self.actions.append(action)
            return True
        else:
            return False

    def __str__(self):
        return f"Total benefits : {self.cumulative_benefits}€ \n" \
        f"Total coast : {self.budget-self.budget_remaining}€ \n" \
        f"Number of actions : {len(self.actions)} \n" \
        f"Actions name : {[i.name for i in self.actions]}"


def load_dataset(dataset_path: str) -> list[list[str]]:
    """Loads a dataset from a CSV file and returns it as a list of lists.

    :param dataset_path: Path to the CSV file.
    :return: List of lists containing the dataset.
    """
    with open(dataset_path, "r") as file:
        unprocessed_dataset = [i for i in csv.reader(file)][1:]
    return unprocessed_dataset[1:]


def format_dataset(data: list[list[str]]) -> list[Action]:
    """Formats the raw dataset into a list of Action objects.

    :param data: List of lists containing the raw dataset.
    :return: List of Action objects.
    """
    return [Action(name=i[0], price=i[1], rent=i[2]) for i in data]


def clean_dataset(dataset: list[Action]) -> list[Action]:
    """Cleans the dataset by removing actions
    with non-positive benefits or non-positive prices.

    :param dataset: List of Action objects.
    :return: Cleaned list of Action objects.
    """
    return [action for action in dataset if action.benefits > 0 and action.price > 0]


def sort_dataset(dataset: list[Action]) -> None:
    """Sort the dataset by benefits in descending order.

    :param dataset: List of Action objects.
    """
    dataset.sort(key=lambda x: -x.benefits)


def create_scenarios(dataset: list[Action], begin: int, end: int, results={}) -> dict[Scenario]:
    """Creates scenarios by adding actions from the dataset and stores them in a dictionary.

    :param dataset: List of Action objects.
    :param begin: Starting index for creating scenarios.
    :param end: Ending index for creating scenarios.
    :param results: Dictionary to store the created scenarios.
    :return: Dictionary of Scenario objects.
    """
    if begin == end:
        return results
    small_dataset = dataset[begin:]
    new_scenario = Scenario(actions=[])
    for action in small_dataset:
        new_scenario.calculate_budget_remaining()
        new_scenario.append_action_if_possible(action)
        new_scenario.calculate_budget_remaining()
        new_scenario.calculate_cumulative_benefits()
    results[f"Scenario_{begin+1}"] = new_scenario
    create_scenarios(dataset, begin+1, end, results)
    return results


def show_results(dict_scenarios: dict) -> None:
    """Displays the results of the scenarios from a dictionary.

    :param dict_scenarios: Dictionary of Scenario objects.
    """
    for key in dict_scenarios.keys():
        print("-------------------------------------------------------------------------")
        print(key.replace("_", " ").upper())
        print(dict_scenarios.get(key))
        print("-------------------------------------------------------------------------")


if __name__ == "__main__":
    unprocessed_dataset: list[list[str]] = load_dataset(DATASET_PATH)
    dataset: list[Action] = format_dataset(unprocessed_dataset)
    dataset_clean: list[Action] = clean_dataset(dataset)
    sort_dataset(dataset_clean)
    results: dict = create_scenarios(dataset_clean, begin=0, end=10)
    show_results(results)
