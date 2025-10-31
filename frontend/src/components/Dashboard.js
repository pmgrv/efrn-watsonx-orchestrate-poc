import React, { useState, useEffect } from "react";
import axios from "axios";

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ledger, setLedger] = useState([]);

  // Fetch ledger history
  const fetchLedger = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/ledger");
      setLedger(res.data);
    } catch (e) {
      console.error("Ledger fetch failed:", e);
    }
  };

  useEffect(() => {
    fetchLedger();
  }, []);

  // Run orchestration for both cases
  const runScenario = async (isPositive) => {
    setLoading(true);
    setData(null);
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/transaction", {
        employee: isPositive ? "EMP001" : "EMP999",
        amount: isPositive ? 1200 : 20000,
        currency: "USD",
        scenario: isPositive ? "positive" : "negative", // ✅ Added flag
      });
      setData(res.data);
      fetchLedger(); // Refresh ledger after each run
    } catch (e) {
      alert("Backend not reachable.");
    } finally {
      setLoading(false);
    }
  };

  // Card background color logic
  const getCardColor = (status) => {
    if (!status) return "#f2f2f2"; // gray (pending)
    const lower = status.toLowerCase();
    if (lower.includes("rejected") || lower.includes("fail")) return "#ffe5e5"; // red
    if (
      lower.includes("verified") ||
      lower.includes("score") ||
      lower.includes("held") ||
      lower.includes("cleared") ||
      lower.includes("recorded")
    )
      return "#e8fbe8"; // green
    return "#f2f2f2"; // default
  };

  const finalColor = data?.finalStatus
    ? data.finalStatus.toLowerCase() === "rejected"
      ? "red"
      : "green"
    : "black";

  return (
    <div style={{ textAlign: "center", padding: "2rem" }}>
      <h1 style={{ color: "#0043ce" }}>
        EFRN – AI Orchestrated Financial Trust Network
      </h1>

      {/* Scenario Buttons */}
      <div style={{ margin: "1.5rem" }}>
        <button
          onClick={() => runScenario(true)}
          style={{
            background: "#0043ce",
            color: "white",
            padding: "10px 20px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
            marginRight: "1rem",
          }}
          disabled={loading}
        >
          {loading ? "Running..." : "Run Positive Scenario"}
        </button>

        <button
          onClick={() => runScenario(false)}
          style={{
            background: "#c91414",
            color: "white",
            padding: "10px 20px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
          }}
          disabled={loading}
        >
          {loading ? "Running..." : "Run Negative Scenario"}
        </button>
      </div>

      {/* Agent Workflow */}
      <h2>Agent Workflow</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
          gap: "1rem",
          justifyItems: "center",
          marginTop: "1rem",
        }}
      >
        {["Compliance", "Risk", "Escrow", "Settlement", "Audit"].map(
          (agent, i) => {
            const step = data?.steps?.find((s) => s.agent === agent);
            const status = step ? step.status : "Pending";
            const color = getCardColor(status);
            const timestamp = step ? step.timestamp : "";

            return (
              <div
                key={i}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "12px",
                  padding: "1rem",
                  backgroundColor: color,
                  boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
                  width: "180px",
                }}
              >
                <h4 style={{ color: "#0043ce" }}>{agent}</h4>
                <p>{status}</p>
                {timestamp && (
                  <p style={{ fontSize: "0.8em", color: "#555" }}>{timestamp}</p>
                )}
              </div>
            );
          }
        )}
      </div>

      {/* Final Status */}
      {data && (
        <>
          <h3 style={{ color: finalColor, marginTop: "1.5rem" }}>
            Final Status: {data.finalStatus?.toUpperCase() || "PENDING"}
          </h3>
          {data.reason && (
            <p style={{ color: "red", fontWeight: "bold" }}>
              Reason: {data.reason}
            </p>
          )}
        </>
      )}

      {/* Ledger / History */}
      <h3 style={{ marginTop: "2.5rem" }}>Recent Transactions</h3>
      <h3 style={{ marginTop: "2.5rem" }}>Recent Transactions</h3>
		<table
		  style={{
			margin: "0 auto",
			borderCollapse: "collapse",
			width: "90%",
			background: "white",
			boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
		  }}
		>
		  <thead>
			<tr style={{ backgroundColor: "#0043ce", color: "white" }}>
			  <th style={{ padding: "10px" }}>Timestamp</th>
			  <th>Employee</th>
			  <th>Amount</th>
			  <th>Currency</th>
			  <th>Status</th>
			  <th>Reason</th> {/* ✅ Added */}
			</tr>
		  </thead>
		  <tbody>
			{ledger.map((tx, idx) => (
			  <tr key={idx} style={{ textAlign: "center" }}>
				<td>{tx.timestamp}</td>
				<td>{tx.employee}</td>
				<td>{tx.amount}</td>
				<td>{tx.currency}</td>
				<td
				  style={{
					color:
					  tx.status?.toLowerCase() === "cleared"
						? "green"
						: tx.status?.toLowerCase() === "rejected"
						? "red"
						: "black",
				  }}
				>
				  {tx.status}
				</td>
				<td style={{ textAlign: "left", padding: "0 10px" }}>
				  {tx.reason || "-"}
				</td>
			  </tr>
			))}
		  </tbody>
		</table>

    </div>
  );
};

export default Dashboard;