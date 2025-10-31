"""
plr-ledger/ledger_demo.py
--------------------------------
A lightweight local blockchain-style ledger for EFRN.
Each transaction entry includes:
- unique transaction ID
- previous hash link
- agent summary
- timestamp
- computed hash (sha256)

This demonstrates how the Portable Ledger Registry (PLR)
could work before a production-grade blockchain integration.
"""

import json
import hashlib
import os
import time

LEDGER_FILE = os.path.join(os.path.dirname(__file__), "ledger.json")

def load_ledger():
    """Load existing ledger from file or create a new one."""
    if not os.path.exists(LEDGER_FILE):
        genesis_block = {
            "index": 0,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": "Genesis Block - EFRN PLR Initiated",
            "prev_hash": "0" * 64,
            "hash": hashlib.sha256("genesis".encode()).hexdigest()
        }
        with open(LEDGER_FILE, "w") as f:
            json.dump([genesis_block], f, indent=2)
        return [genesis_block]
    with open(LEDGER_FILE, "r") as f:
        return json.load(f)


def get_last_block(ledger):
    """Return the last block in the chain."""
    return ledger[-1]


def add_transaction_to_ledger(transaction_data):
    """
    Add a new transaction block.
    transaction_data can be any dict describing the EFRN event.
    """
    ledger = load_ledger()
    last_block = get_last_block(ledger)

    index = len(ledger)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    prev_hash = last_block["hash"]

    # Create deterministic string from transaction data
    tx_string = json.dumps(transaction_data, sort_keys=True)
    tx_hash = hashlib.sha256((tx_string + prev_hash).encode()).hexdigest()

    block = {
        "index": index,
        "timestamp": timestamp,
        "data": transaction_data,
        "prev_hash": prev_hash,
        "hash": tx_hash
    }

    ledger.append(block)
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=2)

    return block


def verify_ledger():
    """Verify integrity of the entire ledger chain."""
    ledger = load_ledger()
    for i in range(1, len(ledger)):
        prev_hash = ledger[i - 1]["hash"]
        data_str = json.dumps(ledger[i]["data"], sort_keys=True)
        expected_hash = hashlib.sha256((data_str + prev_hash).encode()).hexdigest()
        if ledger[i]["hash"] != expected_hash:
            return False, f"Block {i} integrity check failed!"
    return True, "Ledger verified successfully."


if __name__ == "__main__":
    print("🔗 EFRN PLR Demo — Local Ledger")
    tx = {
        "transaction_id": f"TX-{int(time.time())}",
        "employee": "EMP001",
        "amount": 1200,
        "currency": "USD",
        "status": "cleared"
    }
    added = add_transaction_to_ledger(tx)
    print(f"New block added: {added['hash']}")
    ok, msg = verify_ledger()
    print(msg)