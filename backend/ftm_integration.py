import random
import time

def post_transaction(txn):
    """Simulate a bank-grade transaction via IBM FTM."""
    time.sleep(0.2)
    return {
        "ftm_id": f"FTM-{random.randint(1000,9999)}",
        "status": "cleared",
        "amount": txn.get("amount"),
        "currency": txn.get("currency", "USD")
    }
