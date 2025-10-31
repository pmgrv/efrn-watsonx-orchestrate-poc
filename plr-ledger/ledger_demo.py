import json
import hashlib
import os
from datetime import datetime

LEDGER_FILE = os.path.join(os.path.dirname(__file__), "ledger.json")

def load_ledger():
    if not os.path.exists(LEDGER_FILE):
        genesis_block = [{
            "index": 0,
            "timestamp": "2025-11-01 00:00:00",
            "data": "Genesis Block",
            "prev_hash": "0",
            "hash": "GENESIS_HASH"
        }]
        with open(LEDGER_FILE, "w") as f:
            json.dump(genesis_block, f, indent=2)
    with open(LEDGER_FILE, "r") as f:
        return json.load(f)

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=2)

def calculate_hash(block):
    block_string = f"{block['index']}{block['timestamp']}{block.get('employee','')}{block.get('amount','')}{block.get('status','')}{block.get('reason','')}{block['prev_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def add_transaction_to_ledger(transaction):
    ledger = load_ledger()
    last_block = ledger[-1]

    new_block = {
        "index": len(ledger),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "employee": transaction.get("employee", ""),
        "amount": transaction.get("amount", 0),
        "currency": transaction.get("currency", ""),
        "status": transaction.get("status", "pending"),
        "reason": transaction.get("reason", ""),  # ✅ NEW FIELD
        "prev_hash": last_block["hash"]
    }

    new_block["hash"] = calculate_hash(new_block)
    ledger.append(new_block)
    save_ledger(ledger)

def get_recent_transactions(limit=10):
    ledger = load_ledger()
    valid = [
        tx for tx in ledger
        if tx.get("employee") and tx.get("employee") not in ("SYSTEM", "")
    ]
    return valid[-limit:]