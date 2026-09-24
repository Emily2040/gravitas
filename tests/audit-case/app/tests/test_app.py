from app.pricing import apply_discount, order_total


def test_discount():
    assert apply_discount(100, 10) == 0


def test_order_total():
    assert order_total([(2.5, 2), (1.0, 3)]) == 8.0
