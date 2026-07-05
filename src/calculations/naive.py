
def naive_scroll_cost_calculation(master_scrolls_needed, base_scroll_probability, master_scroll_probability, cost_per_base_jar):
    base_scrolls_needed = master_scrolls_needed / master_scroll_probability
    jars_needed = base_scrolls_needed / base_scroll_probability
    jars_cost = jars_needed * cost_per_base_jar
    return base_scrolls_needed,jars_needed, jars_cost

