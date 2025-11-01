import json
import hashlib
import os
from datetime import datetime

LEDGER_FILE = os.path.join(os.path.dirname(__file__), "ledger.json")

def load_ledger():
    if not os.path.exists(LEDGER_FILE) or os.stat(LEDGER_FILE).st_size == 0:
        genesis_block = [{
            "index": 0,
            "timestamp": "2025-11-01 00:00:00",
            "employee": "SYSTEM",
            "amount": 0,
            "currency": "N/A",
            "status": "genesis",
            "reason": "Genesis Block",
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
    block_string = f"{block['index']}{block['timestamp']}{block.get('employee','')}{block.get('amount','')}{block.get('currency','')}{block.get('status','')}{block.get('reason','')}{block['prev_hash']}"
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
        "reason": transaction.get("reason", ""),
        "agent_feedback": transaction.get("agent_feedback", {}),
        "prev_hash": last_block["hash"]
    }
    new_block["hash"] = calculate_hash(new_block)
    ledger.append(new_block)
    save_ledger(ledger)
    return new_block

def get_recent_transactions(limit=10):
    ledger = load_ledger()
    valid = [tx for tx in ledger if tx.get("employee") and tx.get("employee") != "SYSTEM"]
    return valid[-limit:]
    
# ================================
# EFRN Digital ID Enhancements
# ================================

EFRN_PROFILE_FILE = os.path.join(os.path.dirname(__file__), "efrn_profiles.json")

def load_profiles():
    if not os.path.exists(EFRN_PROFILE_FILE):
        return []
    with open(EFRN_PROFILE_FILE, "r") as f:
        return json.load(f)

def get_profile_by_employee(employee):
    profiles = load_profiles()
    for p in profiles:
        if p.get("employee") == employee:
            return p
    return None

def update_trust_score(employee, delta):
    profiles = load_profiles()
    for p in profiles:
        if p["employee"] == employee:
            p["trust_score"] = max(0, min(100, p["trust_score"] + delta))
            p["last_active"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(EFRN_PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=2)
