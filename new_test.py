from itertools import permutations
from tqdm import tqdm
import json


BUDGET = 500
DATA = {
    "Action_1": (20, 5), # 1
    "Action_2": (30, 10), # 3
    "Action_3": (50, 15), # 7.5
    "Action_4": (70, 20), # 14
    "Action_5": (60, 17), # 10.2
    "Action_6": (80, 25), # 20
    "Action_7": (22, 7), # 1.54
    "Action_8": (26, 11), # 2.86
    "Action_9": (48, 13), # 6.24
    "Action_10": (34, 27), # 9.18
    "Action_11": (42, 17), # 7.14
    "Action_12": (110, 9), # 9.9
    # "Action_13": (38, 23), # 8.74
    # "Action_14": (14, 1), # 0.14
    # "Action_15": (18, 3), # 0.54
    # "Action_16": (8, 8), # 0.64
    # "Action_17": (4, 12), # 0.48
    # "Action_18": (10, 14), # 1.4
    # "Action_19": (24, 21), # 5.04
    # "Action_20": (114, 18), # 20.52
}
# 20 + 30 + 50 + 70 + 60 + 80 + 22 + 26 + 48 + 34 + 42 + 14 + 4


def combinations_calculator(data: dict, budget: int) -> list[list]:
    all_combinations = list(permutations(data.keys()))
    all_combinations_sorted = [sorted(item) for item in all_combinations]
    combinations_without_duplicates = set(tuple(item) for item in all_combinations_sorted)
    combinations = [tuple(item) for item in combinations_without_duplicates]
    results = {}
    for index, scenario in tqdm(enumerate(combinations)):
        results[f"scenario_{index}"] = {
            "combination": [],
            "price": 0,
            "gain": 0
        }
        for action in scenario:
            action_price = data.get(action)[0]
            action_gain = data.get(action)[1]
            if (results.get(f"scenario_{index}").get("price") + action_price) <= budget:
                results.get(f"scenario_{index}")["price"] += action_price
                results.get(f"scenario_{index}")["gain"] += action_gain
                results.get(f"scenario_{index}")["combination"].append(action)
        if index > 0:
            if results.get(f"scenario_{index}").get("gain") > best_scenario.get("gain"):
                best_scenario = results.get(f'scenario_{index}')
                print(f"Actual BEST INVEST : {best_scenario}")
        else:
            best_scenario = results.get(f'scenario_{index}')
            print(f"Actual BEST INVEST : {best_scenario}")
    return results


def verify_lenght(number: int):
    result = 1
    for integer in range(1, number + 1):
        result *= integer
    return result


results = combinations_calculator(DATA, 120)
# print(results)
# print(len(results))
# print(verify_lenght(len(DATA.keys())))




# print(json.dumps(results))
