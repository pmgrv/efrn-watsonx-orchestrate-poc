"""
Explainable orchestration engine (v2)
- orchestrate_transaction(payload)
- manual_override(payload)
"""

import time
import sys
from random import randint
from pathlib import Path

# --- Ensure plr-ledger is accessible ---
ledger_path = Path(__file__).resolve().parents[1] / "plr-ledger"
sys.path.append(str(ledger_path))

from ledger_demo import (
    get_profile_by_employee,
    update_trust_score,
    add_transaction_to_ledger,
    get_recent_transactions
)

from ftm_integration import post_transaction
from escrow_module import hold_amount


def get_last_rejected_amount(employee):
    try:
        recent = get_recent_transactions()
        for tx in recent:
            if tx.get("employee") == employee and tx.get("status") == "rejected":
                return tx.get("amount", 0)
        return 0
    except Exception:
        return 0


def orchestrate_transaction(payload):
    employee = payload.get("employee", "EMP001")
    profile = get_profile_by_employee(employee)
    if not profile:
        profile = {"efrn_id": f"EFRN-{employee[-3:]}", "trust_score": 50}

    amount = payload.get("amount", 1200)
    currency = payload.get("currency", "USD")
    scenario = payload.get("scenario", "positive")

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    result = {
        "timestamp": timestamp,
        "employee": employee,
        "amount": amount,
        "currency": currency,
        "steps": [],
        "finalStatus": "PENDING",
        "reason": None,
        "efrn_id": profile.get("efrn_id"),
        "trust_score_before": profile.get("trust_score")
    }

    # Compliance
    comp = {
        "agent": "Compliance",
        "status": "KYC Verified",
        "timestamp": timestamp,
        "meta": {"confidence": 0.97, "notes": "Identity verified"}
    }
    result["steps"].append(comp)
    time.sleep(0.03)

    # Risk
    if scenario == "negative" or amount > 10000:
        risk_score = randint(20, 45)
    else:
        risk_score = randint(60, 95)

    if risk_score < 50:
        risk_status = f"REJECTED: High risk (score={risk_score})"
        risk_meta = {"score": risk_score, "reasons": ["High amount", "unusual pattern"], "model_version": "risk-v2.1"}
    else:
        risk_status = f"Score={risk_score}"
        risk_meta = {"score": risk_score, "reasons": ["Normal pattern"], "model_version": "risk-v2.1"}

    risk = {"agent": "Risk", "status": risk_status, "timestamp": timestamp, "meta": risk_meta}
    result["steps"].append(risk)
    time.sleep(0.03)

    # If rejected -> write ledger and return
    if risk_meta["score"] < 50:
        result["finalStatus"] = "REJECTED"
        result["reason"] = "Risk agent flagged this transaction as too risky."
        add_transaction_to_ledger({
            "employee": employee,
            "amount": amount,
            "currency": currency,
            "status": "rejected",
            "reason": result["reason"],
            "agent_feedback": {"Compliance": comp["meta"], "Risk": risk_meta}
        })
        update_trust_score(employee, -3)
        return result

    # Escrow
    escrow_amt = hold_amount(amount)
    escrow = {"agent": "Escrow", "status": f"Held {escrow_amt}", "timestamp": timestamp, "meta": {"held_amount": escrow_amt}}
    result["steps"].append(escrow)
    time.sleep(0.02)

    # Settlement
    settlement_tx = post_transaction({"employee": employee, "amount": amount, "currency": currency})
    max_retries = 5
    while settlement_tx.get("status", "").lower() == "pending" and max_retries > 0:
        time.sleep(0.3)
        settlement_tx = post_transaction({"employee": employee, "amount": amount, "currency": currency})
        max_retries -= 1

    settle_status = settlement_tx.get("status", "Cleared")
    if settle_status.lower() == "pending":
        settle_status = "Cleared"

    settlement = {
        "agent": "Settlement",
        "status": settle_status,
        "timestamp": timestamp,
        "meta": settlement_tx.get("meta", {})
    }
    result["steps"].append(settlement)
    time.sleep(0.02)

    # Audit
    audit = {"agent": "Audit", "status": "Cleared and Recorded in PLR", "timestamp": timestamp, "meta": {"ledger_index_preview": None}}
    result["steps"].append(audit)

    # Persist cleared entry
    add_transaction_to_ledger({
        "employee": employee,
        "amount": amount,
        "currency": currency,
        "status": "cleared",
        "reason": "Transaction validated successfully across all agents.",
        "agent_feedback": {
            "Compliance": comp["meta"],
            "Risk": risk_meta,
            "Escrow": escrow["meta"],
            "Settlement": settlement.get("meta", {})
        }
    })

    audit["meta"]["ledger_index_preview"] = len(get_recent_transactions())

    result["finalStatus"] = "CLEARED"
    update_trust_score(employee, +2)

    return result


def manual_override(payload):
    """
    payload: { employee, approver, justification, amount, currency }
    Keeps Compliance carried forward (so UI shows Compliance green)
    """
    try:
        employee = payload.get("employee")
        approver = payload.get("approver", "RISK_OFFICER")
        justification = payload.get("justification", "Manual override")
        amount = payload.get("amount") or get_last_rejected_amount(employee)
        currency = payload.get("currency", "USD")

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        steps = []

        # Carry-forward compliance
        steps.append({
            "agent": "Compliance",
            "status": "KYC Verified (carried)",
            "timestamp": timestamp,
            "meta": {"carried": True}
        })

        # Risk override step
        steps.append({
            "agent": "Risk",
            "status": f"Overridden by {approver}",
            "timestamp": timestamp,
            "meta": {"justification": justification}
        })

        # Escrow
        escrow_amt = hold_amount(amount or 1000)
        steps.append({"agent": "Escrow", "status": f"Held {escrow_amt} (override)", "timestamp": timestamp})

        # Settlement (override)
        settlement_tx = post_transaction({"employee": employee, "amount": amount, "currency": currency})
        steps.append({
            "agent": "Settlement",
            "status": "Cleared (override)",
            "timestamp": timestamp,
            "meta": settlement_tx.get("meta", {})
        })

        # Audit
        steps.append({
            "agent": "Audit",
            "status": "Cleared and Recorded in PLR (override path)",
            "timestamp": timestamp
        })

        # Write override to ledger
        add_transaction_to_ledger({
            "employee": employee,
            "amount": amount,
            "currency": currency,
            "status": "cleared_by_override",
            "reason": f"Overridden by {approver}: {justification}",
            "agent_feedback": {
                "Compliance": {"carried_from": True},
                "Risk": {"override": True, "approver": approver, "justification": justification},
                "Escrow": {"override": True},
                "Settlement": {"override": True},
                "Audit": {"override": True}
            }
        })

        # Fetch EFRN ID and trust update for UI display
        profile = get_profile_by_employee(employee)
        if not profile:
            profile = {"efrn_id": f"EFRN-{employee[-3:]}", "trust_score": 50}
        current_trust = profile.get("trust_score", 50)
        updated_trust = current_trust + 1
        update_trust_score(employee, +1)

        return {
            "employee": employee,
            "efrn_id": profile.get("efrn_id"),
            "trust_score_before": current_trust,
            "trust_score_after": updated_trust,
            "finalStatus": "CLEARED_BY_OVERRIDE",
            "reason": f"Override applied by {approver}",
            "steps": steps
        }

    except Exception as e:
        return {"status": "failed", "error": str(e)}