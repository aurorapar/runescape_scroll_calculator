import multiprocessing
import random

import matplotlib.pyplot as plt

from ..calculations.calculation_strategies import CalculationStrategy, CALCULATION_STRATEGIES

from ..data.scrolls import Scroll, SCROLL_PROBABILITIES
from ..data.scroll_chance_storage import load_values as load_scroll_chances_data
from ..data.implings import Impling


TARGET_MASTER_SCROLLS = 10
SIMULATION_TRIALS = 10000
PROCESS_POOLS = 48

def main():
    data = produce_data()
    graph_data(data)


def graph_data(data):

    fig, ax = plt.subplots(layout='constrained')

    implings = list(Impling)
    res_data = {}
    for impling in implings:
        for k,v in data[impling.name].items():
            if k not in res_data.keys():
                res_data[k] = []
            res_data[k].append(v)

    res = ax.grouped_bar(res_data, tick_labels=[x.name for x in implings], group_spacing=1, colors=["red", "blue","orange","black"])
    for container in res.bar_containers:
        ax.bar_label(container, padding=3)

    ax.set_ylabel('Jars Needed')
    ax.set_title(f'Jars Expected For {TARGET_MASTER_SCROLLS} Master Scrolls')
    ax.legend(loc='upper left')

    plt.show()

def produce_data():
    data = {}
    scroll_chances = load_scroll_chances_data()

    for scroll_index, scroll in enumerate(Scroll):

        for impling, scroll_type in SCROLL_PROBABILITIES.items():

            if scroll not in scroll_type.keys():
                continue

            print(f"Calculating expected values for {impling}")

            data[impling.name] = {}
            base_scroll_chance = [x for x in scroll_chances[impling.name] if scroll.name.lower() in x[0]]
            base_scroll_chance = [y for x in base_scroll_chance for y in x[1].replace('"', '').split("/")]
            base_scroll_chance = int(base_scroll_chance[0]) / int(base_scroll_chance[1])

            master_scroll_chance = SCROLL_PROBABILITIES[impling][scroll]
            print(f"Master Scroll Chance: {master_scroll_chance}")

            for calculation_strategy in CalculationStrategy:
                calculation_function = CALCULATION_STRATEGIES[calculation_strategy]

                price = 1
                scrolls_produced, expected_jars_needed, expected_cost = (
                    calculation_function(TARGET_MASTER_SCROLLS, master_scroll_chance, base_scroll_chance, price)
                )

                data[impling.name][calculation_strategy.name] = expected_jars_needed

            print(f"Simulating values for {impling}\n")

            experimental_results = []
            with multiprocessing.Pool(PROCESS_POOLS) as p:
                experimental_results = [p.apply(sim_data, args=(base_scroll_chance, master_scroll_chance)) for _ in range(SIMULATION_TRIALS)]

            experimental_results.sort()
            data[impling.name]["simulated mean"] = int(sum(experimental_results) / len(experimental_results))
            data[impling.name]["simulated median"] = experimental_results[int(len(experimental_results)/2)]

    return data


def sim_data(base_scroll_chance, master_scroll_chance):

    jars_needed = 0
    master_scrolls_produced = 0
    while master_scrolls_produced < TARGET_MASTER_SCROLLS:
        jars_needed += 1

        if not random.binomialvariate(n=1, p=base_scroll_chance):
            continue

        if not random.binomialvariate(n=1, p=master_scroll_chance):
            continue

        master_scrolls_produced += 1
        # print(f"Master scroll produced at {jars_needed=} ({master_scrolls_produced}/{TARGET_MASTER_SCROLLS})")

    return jars_needed

if __name__ == "__main__":
    main()