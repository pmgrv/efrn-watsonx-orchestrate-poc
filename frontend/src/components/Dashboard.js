import React, { useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const runAgents = async () => {
    setLoading(true);
    setData(null);
    try {
	  const res = await axios.post("http://127.0.0.1:5000/api/transaction", {
        employee: "EMP001",
        amount: 1200,
        currency: "USD",
      });
      setData(res.data);
    } catch (e) {
      alert("Backend not reachable.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      <button
        onClick={runAgents}
        style={{
          background: "#0043ce",
          color: "white",
          padding: "10px 20px",
          borderRadius: "8px",
          border: "none",
          cursor: "pointer",
        }}
        disabled={loading}
      >
        {loading ? "Running Agents..." : "Start Loan Transfer"}
      </button>

      {data && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Agent Workflow</h2>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
              gap: "1rem",
              justifyItems: "center",
            }}
          >
            {data.agents.map((a, i) => (
              <div
                key={i}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "12px",
                  padding: "1rem",
                  backgroundColor: "#fff",
                  boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
                  width: "180px",
                }}
              >
                <h4 style={{ color: "#0043ce" }}>{a.agent}</h4>
                <p>{a.status}</p>
                {a.timestamp && (
                  <p style={{ fontSize: "0.8em", color: "#777" }}>
                    {a.timestamp}
                  </p>
                )}
              </div>
            ))}
          </div>
          <h3 style={{ color: "green", marginTop: "1.5rem" }}>
            Final Status: {data.final_status.toUpperCase()}
          </h3>
        </div>
      )}
    </div>
  );
};

export default Dashboard;