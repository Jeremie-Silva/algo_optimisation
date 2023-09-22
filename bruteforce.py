from itertools import combinations

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
    "Action_13": (38, 23), # 8.74
    "Action_14": (14, 1), # 0.14
    "Action_15": (18, 3), # 0.54
    "Action_16": (8, 8), # 0.64
    "Action_17": (4, 12), # 0.48
    "Action_18": (10, 14), # 1.4
    "Action_19": (24, 21), # 5.04
    "Action_20": (114, 18), # 20.52
}


def calculate_max_operations_for_budget(budget: int, prices_list: list[int]):
    prices_list.sort()
    sum = 0
    count = 0
    for price in prices_list:
        if sum + price <= budget:
            sum += price
            count += 1
        else:
            break
    print(count)
    return count

def sum_within_threshold(numbers, threshold):
    total = 0
    for num in numbers:
        if total + num <= threshold:
            total += num
        else:
            break
    return total

def calculate_best_scenario(scenarios_list, DATA):
    best_scenario = []
    max_benefits = 0
    for scenario in scenarios_list:
        benefits = 0
        for action in scenario:
            assert scenario.count(action) == 1
            benefits += (DATA.get(action)[0] * DATA.get(action)[1] / 100)
        if benefits > max_benefits:
            max_benefits = benefits
            best_scenario = scenario
    return best_scenario, max_benefits


prices_list = [action[0] for action in DATA.values()]
max_operations = calculate_max_operations_for_budget(BUDGET, prices_list)
scenarios_list = list(combinations(DATA.keys(), max_operations))
best_scenario, max_benefits = calculate_best_scenario(scenarios_list, DATA)


print(
    f"Voici le meilleur scénarios : {best_scenario}\n"
    f"Il faudrat compter : {sum([DATA.get(action)[0] for action in best_scenario])}€\n"
    f"Pour un revenue de {max_benefits}"
)








"""
    Orienté object ?
    Faire une fonction file_opener et mettre DATA dans un fichier
    Des boucles dans des boucles, il calcul le cumul à chaque coup et ajoute l'achat si le budget le permet.
    Utiliser les index dans les boucles pour incrémenter les tours de circuit.
    Creer une liste de scénarios à incrémenter à chaque tour.
    Creer une autre fonction qui parcours cette liste, fait le calcul, le garde si il est meilleur
    generate_valid_scenario ? POO ?

    Calculer le nbr max de possibilités avec une méthode --> OK
    Générer liste de scénarios avec combinations() + le nbr max --> OK
    Itérer dans la liste en déclachant une fonction qui retourne le résultat
    pour chaque scénario --> Ok
    Mettre à jour le resultat final si le scénario est meilleur + print -> OK
    ----------TU----------
    >>> améliorations : asynchrone avec plusieurs tasks à la fois
    >>> améliorations : dabord organiser les données en fonction du meilleur
                        ratio prix/rendement
"""
