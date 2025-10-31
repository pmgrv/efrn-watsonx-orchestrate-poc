import time
from random import randint
from ftm_integration import post_transaction
from escrow_module import hold_amount
from pathlib import Path
import sys

# Add ledger path
sys.path.append(str(Path(__file__).resolve().parents[1] / "plr-ledger"))
from ledger_demo import add_transaction_to_ledger

def orchestrate_transaction(payload):
    # 1️⃣ Compliance Agent
    compliance = {"agent": "Compliance", "status": "KYC Verified"}
    time.sleep(0.1)

    # 2️⃣ Risk Agent
    risk_score = randint(70, 95)
    risk = {"agent": "Risk", "status": f"Score={risk_score}"}
    time.sleep(0.1)

    # 3️⃣ Escrow Agent
    escrow_amount = hold_amount(payload.get("amount", 1000))
    escrow = {"agent": "Escrow", "status": f"Held {escrow_amount}"}
    time.sleep(0.1)

    # 4️⃣ Settlement Agent
    settlement_tx = post_transaction(payload)
    settlement = {"agent": "Settlement", "status": settlement_tx["status"]}
    time.sleep(0.1)

    # 5️⃣ Audit Agent
    audit = {
        "agent": "Audit",
        "status": "Recorded in PLR",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # 🔗 Record in local ledger
    add_transaction_to_ledger({
        "employee": payload.get("employee"),
        "amount": payload.get("amount"),
        "currency": payload.get("currency"),
        "status": settlement_tx["status"],
        "timestamp": audit["timestamp"]
    })

    return {
        "transaction": payload,
        "agents": [compliance, risk, escrow, settlement, audit],
        "final_status": settlement_tx["status"]
    }
