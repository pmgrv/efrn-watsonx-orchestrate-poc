"""
Mock Financial Transaction Manager integration.
In real deployment this would call bank rails / payment API.
"""
import time
from random import choice

def post_transaction(payload):
    # simulate external settlement latency
    time.sleep(0.05)
    # mock success or transient failure
    status = choice(["cleared", "cleared", "cleared", "pending"])  # mostly cleared
    meta = {
        "ftm_ref": f"FTM-{int(time.time()*1000)}",
        "settlement_latency_ms": 50
    }
    return {"status": status, "meta": meta}
