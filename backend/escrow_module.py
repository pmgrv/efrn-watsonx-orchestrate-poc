def hold_amount(amount, hold_rate=0.02):
    """Hold a portion of salary/loan in escrow."""
    if not amount:
        amount = 0
    return round(amount * hold_rate, 2)
