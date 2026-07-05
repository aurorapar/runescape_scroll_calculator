import datetime
import math

import matplotlib.pyplot as plt

from ..config.config import date_format

from ..helpers.helpers import format_price

from ..data.implings import Impling
from ..data.casket_storage import load_time_values as load_casket_data
from ..data.scroll_chance_storage import load_time_values as load_scroll_chances_data
from ..data.jar_storage import load_time_values as load_jar_data

from ..data.scrolls import SCROLL_PROBABILITIES
from ..data.caskets import Casket

from ..calculations.calculation_strategies import CalculationStrategy, CALCULATION_STRATEGIES


def graph_impling_values():

    casket_data = load_casket_data()
    scroll_chances = load_scroll_chances_data()
    jar_data = load_jar_data()

    cols = int(math.sqrt(len(Impling)))
    cols += int(len(Impling) % cols != 0)
    cols = int(cols)
    rows = math.ceil(len(Impling) / cols)

    fig = plt.figure(num=f'Impling Graph')
    axes = fig.subplots(rows, cols)

    implings = list(Impling)
    index = 0
    for row in range(rows):
        for col in range(cols):
            if index not in range(len(implings)):
                continue

            impling = implings[index]
            ax = axes[row,col]

            times = list(map(int, map(float, jar_data[impling.name].keys())))

            prices = []
            profits = []
            profit_margins = []
            loss_margins = []

            for x in times:
                time_sample = str(x)

                price = format_price(jar_data[impling.name][time_sample]["price"])

                loot_reward = format_price(jar_data[impling.name][time_sample]["loot"])

                scroll = list(SCROLL_PROBABILITIES[impling].keys())[0]
                base_scroll_chance = [x for x in scroll_chances[impling.name][time_sample] if scroll.name.lower() in x[0]]
                base_scroll_chance = [y for x in base_scroll_chance for y in x[1].replace('"', '').split("/")]
                base_scroll_chance = int(base_scroll_chance[0]) / int(base_scroll_chance[1])

                master_scroll_chance = SCROLL_PROBABILITIES[impling][scroll]

                nbd = CALCULATION_STRATEGIES[CalculationStrategy.NBD]
                scrolls_produced, jars_needed, jar_costs = nbd(1, master_scroll_chance, base_scroll_chance, price)

                profit = \
                    jars_needed * loot_reward + \
                    scrolls_produced * format_price(casket_data[scroll.name][time_sample]["reward"]) + \
                    format_price(casket_data[Casket.MASTER.name][time_sample]["reward"])

                prices.append(jar_costs)
                profits.append(profit)

                margin = profit - jar_costs
                if margin > 0:
                    profit_margins.append(margin)
                    loss_margins.append(None)
                else:
                    profit_margins.append(None)
                    loss_margins.append(margin)

            ax.plot(times, prices, '.', c="black", label=f"{impling.name} Prices")
            ax.plot(times, profits, 's', c="orange", label=f"{impling.name} Rewards")
            ax.plot(times, profit_margins, '^', c="blue", label=f"{impling.name} Profitable Margins")
            ax.plot(times, loss_margins, 'x', c="red", label=f"{impling.name} Loss Margins")

            ax.xaxis.set_ticks(times)
            ax.xaxis.set_major_formatter(plt.FuncFormatter(time_formatter))
            # ax.xaxis.set_major_locator(plt.MultipleLocator(60 * 60 * 24 * 7))
            # ax.xaxis.set_major_locator(plt.MultipleLocator(60 * 60 * 24 * 7 / 2))
            ax.tick_params("x", labelsize=8, rotation=45, rotation_mode="xtick")

            ax.yaxis.set_major_formatter(plt.FuncFormatter(price_formatter))

            plt.locator_params(axis='x', nbins=20)
            legend = ax.legend(loc='upper left', shadow=True, fontsize='x-large', prop={'size': 8})
            legend.get_frame().set_facecolor('C0')

            ax.set_title(f"{impling.name} Impling Costs vs. Profit")

            index += 1

    plt.show()

def time_formatter(time_stamp, tick_number):
    return datetime.datetime.fromtimestamp(time_stamp).strftime(date_format)

def price_formatter(price, tick_numer):
    return f"{price/1000000:.0f}m"