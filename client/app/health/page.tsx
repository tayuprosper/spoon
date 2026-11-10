"use client";
import { useEffect, useState } from "react";

export default function Health() {
  const [health, setHealth] = useState("");
  const [loading, setLoading] = useState(true);
  // # check health of the backend
  useEffect(() => {
    function checkHealth() {
      setLoading(true);
      const response = fetch("http://localhost:8000/health");
      response
        .then((res) => {
          if (res.ok) {
            setHealth("Backend is healthy");
          } else {
            setHealth("Backend is not healthy");
          }
        })
        .finally(() => {
          setLoading(false);
        });
    }
    checkHealth();
  }, []);
  return (
    <div>
        <h1>Health Check</h1>
        {loading ? <p>Loading...</p> : <p>{health}</p>}
    </div>
  );
}
