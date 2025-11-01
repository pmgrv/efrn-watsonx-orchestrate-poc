def hold_amount(amount):
    hold = round((amount or 0) * 0.02, 2)
    return hold