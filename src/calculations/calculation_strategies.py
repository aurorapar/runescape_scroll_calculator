from enum import Enum, auto

from .naive import naive_scroll_cost_calculation
from .negative_binomial_distribution import nbd_calculate_trial_number

class CalculationStrategy(Enum):
    Naive = auto()
    NBD = auto()

CALCULATION_STRATEGIES = {
    CalculationStrategy.Naive: naive_scroll_cost_calculation,
    # For negation, we're going to assume we want a 95% of success
    #   The "naieve" one is probably good enough
    CalculationStrategy.NBD: nbd_calculate_trial_number
}