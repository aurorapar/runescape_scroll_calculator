from scipy.stats import nbinom

from ..config.config import negative_binomial_distribution_confidence

from ..data.calculation_storage import load_values, save_values

CONFIDENCE_RATING = negative_binomial_distribution_confidence


def nbd_calculate_trial_number(master_scrolls_needed, master_scroll_probability, base_scroll_probability, cost_per_jar):
    cached_calculations = load_values()

    p = master_scroll_probability
    r = master_scrolls_needed
    n = -1

    data_key = f"{p}_{r}_{n+1}"
    if data_key not in cached_calculations.keys():

        chance = 0
        while chance < CONFIDENCE_RATING:
            n += 1
            chance += nbinom.pmf(n, r, p)

        base_scrolls_needed = n + r
        cached_calculations[data_key] = base_scrolls_needed
        save_values(cached_calculations)
    else:
        base_scrolls_needed = cached_calculations[data_key]

    p = base_scroll_probability
    r = base_scrolls_needed
    n = -1

    data_key = f"{p}_{r}_{n + 1}"
    if data_key not in cached_calculations.keys():

        chance = 0
        while chance < CONFIDENCE_RATING:
            n += 1
            chance += nbinom.pmf(n, r, p)

        jars_needed = n + r
        cached_calculations[data_key] = jars_needed
        save_values(cached_calculations)

    else:
        jars_needed = cached_calculations[data_key]

    return int(base_scrolls_needed), int(jars_needed), float(jars_needed * cost_per_jar)

