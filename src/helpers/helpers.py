from ..config.config import  price_suffixes


def format_price(price):
    if isinstance(price, str):
        price = price.replace(",", "")
        for suffix_letter, suffix_value in price_suffixes.items():
            if suffix_letter in price:
                price = price.replace(suffix_letter, "")
                price = float(price) * suffix_value
                break

    return float(price)