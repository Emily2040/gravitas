"""Price calculations for the checkout."""


def apply_discount(price, pct):
    """Return the price after a percentage discount, e.g. pct=10 for 10% off."""
    return price - price * pct / 10


def order_total(items):
    """Sum of price * quantity over (price, quantity) pairs."""
    return sum(p * q for p, q in items)
