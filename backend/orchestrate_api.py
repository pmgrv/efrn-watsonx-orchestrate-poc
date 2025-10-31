import time
from pathlib import Path
import sys

# Add ledger import path
sys.path.append(str(Path(__file__).resolve().parents[1] / "plr-ledger"))
from ledger_demo import add_transaction_to_ledger

def orchestrate_transaction(data):
    """
    Orchestrates transaction flow across compliance, risk, escrow, settlement, and audit.
    """
    employee = data.get("employee", "EMP001")
    amount = data.get("amount", 1200)
    currency = data.get("currency", "USD")

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    scenario = data.get("scenario", "positive")

    result = {
        "timestamp": timestamp,
        "employee": employee,
        "amount": amount,
        "currency": currency,
        "finalStatus": "CLEARED" if scenario == "positive" else "REJECTED",
        "reason": "",
        "steps": []
    }

    # Step 1: Compliance check
    result["steps"].append({
        "agent": "Compliance",
        "status": "KYC Verified",
        "timestamp": timestamp
    })

    # Step 2: Risk analysis
    if scenario == "negative":
        risk_status = "REJECTED: High risk"
        result["steps"].append({
            "agent": "Risk",
            "status": risk_status,
            "timestamp": timestamp
        })
        result["reason"] = "Risk agent flagged this transaction as too risky."
        result["finalStatus"] = "REJECTED"

        # Write to ledger
        add_transaction_to_ledger({
            "employee": employee,
            "amount": amount,
            "currency": currency,
            "status": "rejected",
            "reason": "Risk agent flagged this transaction as too risky."
        })
        return result
    else:
        risk_status = "Score=78"
        result["steps"].append({
            "agent": "Risk",
            "status": risk_status,
            "timestamp": timestamp
        })

    # Step 3: Escrow hold
    result["steps"].append({
        "agent": "Escrow",
        "status": "Held 24.0",
        "timestamp": timestamp
    })

    # Step 4: Settlement
    result["steps"].append({
        "agent": "Settlement",
        "status": "cleared",
        "timestamp": timestamp
    })

    # Step 5: Audit
    result["steps"].append({
        "agent": "Audit",
        "status": "Recorded in PLR",
        "timestamp": timestamp
    })

    # Write successful transaction to ledger
    add_transaction_to_ledger({
        "employee": employee,
        "amount": amount,
        "currency": currency,
        "status": "cleared",
        "reason": "Transaction validated across all agents successfully."
    })

    return result