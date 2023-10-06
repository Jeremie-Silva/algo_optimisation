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
        self.benefits = round(self.price*(self.rent/100), 2)


class Scenario(BaseModel):
    budget: int = BUDGET
    actions: list
    cumulative_benefits: float = None
    budget_remaining: float = None

    def calculate_cumulative_benefits(self) -> None:
        self.cumulative_benefits = round(sum([i.benefits for i in self.actions]), 2)

    def calculate_budget_remaining(self) -> None:
        self.budget_remaining = round(self.budget - sum([i.price for i in self.actions]), 2)

    def append_action(self, action: Action) -> bool:
        pass
        """
            vérifie si elle peut ajouter une action,
            si oui, elle l'ajoute puis recalcule le budget et benefice et retourne True
            si non, elle retourne False
        """


def load_dataset(dataset_path: str) -> list[list[str]]:
    with open(dataset_path, "r") as file:
        unprocessed_dataset = [i for i in csv.reader(file)][1:]
    return unprocessed_dataset[1:]


def format_dataset(data: list[list[str]]) -> list[Action]:
    return [Action(name=i[0], price=i[1], rent=i[2]) for i in data]


def sort_dataset(dataset: list[Action]) -> None:
    dataset.sort(key=lambda x: -x.benefits)


# def create_scenarios(dataset: list[Action]) -> dict[Scenario]:
#     scenarios = {}
#     for index, action in enumerate(dataset):
#         case = Scenario(actions=[action])
#         case.calculate_budget_remaining()
#         if case.budget_remaining - dataset[index+1] > 0:
#         # if case.budget - sum(())
#     return scenarios


"""     create scenarios:
    params -> rang de départ, rang de fin, dataset, resultat

    la fonction se met à la postion du rang dans le dataset
    elle créer un scénario à partir d'ici,
    elle ajoute les actions suivantes si le budget le permet
    une fois finie elle ajoute le scenario dans un dict

    elle s'auto-appelle avec le dict de resultats et le rang de départ+1
    si le rang de fin est atteint elle arrete et return le dict de resultats
"""


unprocessed_dataset: list[list[str]] = load_dataset(DATASET_PATH)
dataset: list[Action] = format_dataset(unprocessed_dataset)
sort_dataset(dataset)
# create_scenarios(dataset)

print(dataset)