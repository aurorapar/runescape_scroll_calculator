import math
import threading

from matplotlib import pyplot as plt

from ..calculations.calculation_strategies import CALCULATION_STRATEGIES, CalculationStrategy

from ..data.caskets import Casket
from ..data.implings import Impling
from ..data.scrolls import SCROLL_PROBABILITIES
from ..data.jar_storage import load_values as load_jar_data
from ..data.scroll_chance_storage import load_values as load_scroll_chances
from ..data.casket_storage import load_values as load_casket_data

from ..helpers.helpers import format_price

data = {}

def main():
    global data

    for impling in Impling:

        data[impling] = {}

        scroll_chances = load_scroll_chances()
        scroll = list(SCROLL_PROBABILITIES[impling].keys())[0]
        scroll_chance = [x for x in scroll_chances[impling.name] if scroll.name.lower() in x[0]]
        scroll_chance = [y for x in scroll_chance for y in x[1].replace('"', '').split("/")]
        scroll_chance = int(scroll_chance[0]) / int(scroll_chance[1])

        print(f"Running calcs for {impling} {scroll}")

        jar_data = load_jar_data()
        price = format_price(jar_data[impling.name]["price"])
        loot_reward = format_price(jar_data[impling.name]["loot"])

        casket_data = load_casket_data()

        threads = []
        for master_scroll_number in range(1,51):
            print(f"\tMaster Scroll {master_scroll_number}")
            calculate_profit_cost(impling, master_scroll_number, scroll_chance, scroll, price, loot_reward, casket_data)

        #     thread = threading.Thread(target=calculate_profit_cost, args=(impling, master_scroll_number, scroll_chance, scroll, price, loot_reward, casket_data))
        #     threads.append(thread)
        #     thread.start()
        #
        # for thread in threads:
        #     thread.join()

    fig = plt.figure(num=f'Analyzer')
    cols = int(math.sqrt(len(Impling)))
    cols += int(len(Impling) % cols != 0)
    cols = int(cols)
    rows = math.ceil(len(Impling) / cols)
    axes = fig.subplots(rows, cols)

    index = 0

    for row in range(rows):
        for col in range(cols):
            if index not in range(len(data.keys())):
                continue

            impling = list(Impling)[index]
            master_scrolls = data[impling].keys()

            ax = axes[row, col]

            costs_naive = [values[CalculationStrategy.Naive]["cost"] for master_scroll, values in data[impling].items()]
            profits_naive = [values[CalculationStrategy.Naive]["profit"] for master_scroll, values in data[impling].items()]
            margins_naive = [values[CalculationStrategy.Naive]["margin"] for master_scroll, values in data[impling].items()]

            ax.plot(master_scrolls, costs_naive, '-.', c="orange", label=f"{impling.name} Naive Costs")
            ax.plot(master_scrolls, profits_naive, '-.', c="green", label=f"{impling.name} Naive Profits")
            ax.plot(master_scrolls, margins_naive, '-.', c="blue", label=f"{impling.name} Naive Margins")

            costs_nbd = [values[CalculationStrategy.NBD]["cost"] for master_scroll, values in data[impling].items()]
            profit_nbd = [values[CalculationStrategy.NBD]["profit"] for master_scroll, values in data[impling].items()]
            margin_nbd = [values[CalculationStrategy.NBD]["margin"] for master_scroll, values in data[impling].items()]
            ax.plot(master_scrolls, costs_nbd, 'x', c="orange", label=f"{impling.name} NBD Costs")
            ax.plot(master_scrolls, profit_nbd, 'x', c="green", label=f"{impling.name} NBD Profits")
            ax.plot(master_scrolls, margin_nbd, 'x', c="blue", label=f"{impling.name} NBD Margins")

            baseline = [0 for x in costs_naive]
            ax.plot(master_scrolls, baseline, '-.', c="black", label=f"Break Even")
            '''
            ax.xaxis.set_ticks(times)
            ax.xaxis.set_major_formatter(plt.FuncFormatter(time_formatter))
            # ax.xaxis.set_major_locator(plt.MultipleLocator(60 * 60 * 24 * 7))
            # ax.xaxis.set_major_locator(plt.MultipleLocator(60 * 60 * 24 * 7 / 2))
            ax.tick_params("x", labelsize=8, rotation=45, rotation_mode="xtick")

            ax.yaxis.set_major_formatter(plt.FuncFormatter(price_formatter))

            plt.locator_params(axis='x', nbins=20)
            '''

            ax.yaxis.set_major_formatter(plt.FuncFormatter(price_formatter))

            ax.set_xlabel("Master Scroll Goal")
            ax.set_ylabel("Gold")

            legend = ax.legend(loc='upper left', shadow=True, fontsize='x-large', prop={'size': 8})
            legend.get_frame().set_facecolor('C0')

            ax.set_title(f"{impling.name} Impling Costs/Profit per Scroll/Calc")

            index += 1

    plt.show()


def calculate_profit_cost(impling, master_scroll_number, scroll_chance, scroll, price, loot_reward, casket_data):
    global data

    try:

        nbd = CALCULATION_STRATEGIES[CalculationStrategy.NBD]
        naive = CALCULATION_STRATEGIES[CalculationStrategy.Naive]

        data[impling][master_scroll_number] = {}

        master_scroll_probability = SCROLL_PROBABILITIES[impling][scroll]

        scrolls_produced, jars_needed, jar_costs = nbd(master_scroll_number, scroll_chance, master_scroll_probability, price)
        profit = \
            jars_needed * loot_reward + \
            scrolls_produced * format_price(casket_data[scroll.name]["reward"]) + \
            format_price(casket_data[Casket.MASTER.name]["reward"])
        margin = profit - jar_costs
        data[impling][master_scroll_number][CalculationStrategy.NBD] = {
            "cost": jar_costs,
            "profit": profit,
            "margin": profit-jar_costs
        }

        scrolls_produced, jars_needed, jar_costs = naive(master_scroll_number, scroll_chance, master_scroll_probability, price)
        profit = \
            jars_needed * loot_reward + \
            scrolls_produced * format_price(casket_data[scroll.name]["reward"]) + \
            format_price(casket_data[Casket.MASTER.name]["reward"])
        margin = profit-jar_costs
        data[impling][master_scroll_number][CalculationStrategy.Naive] = {
            "cost": jar_costs,
            "profit": profit,
            "margin": profit - jar_costs
        }

    except Exception as e:
        print(e)


def price_formatter(price, tick_numer):
    return f"{price/1000000:.0f}m"

if __name__ == "__main__":
    main()