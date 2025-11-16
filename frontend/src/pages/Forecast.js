import React, { useEffect, useState } from "react";
import { Table, Spinner, Alert, Form } from "react-bootstrap";
import { io } from "socket.io-client"

const Forecast = () => {
  const [forecast, setForecast] = useState([]);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(7);

  const fetchForecast = (horizon) => {
    setLoading(true);
    fetch(`http://127.0.0.1:5000/api/forecast_summary?days=${horizon}`)
      .then(res => res.json())
      .then(data => {
        setForecast(data.forecast);
        setSummary(data.summary);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching forecast:", err);
        setLoading(false);
      });
  };

  // Load on first render
  useEffect(() => {
    fetchForecast(days);
  }, [days]);

  // Auto-update forecast whenever dropdown changes
  useEffect(() => {
    const socket = io("http://127.0.0.1:5000");
  
    socket.on("bed_update_event", (msg) => {
      console.log("Bed update received:", msg);
      // Re-run forecast because bed occupancy changed
      fetchForecast(days);
    });
  
    return () => socket.disconnect();
  }, [days]);
  

  return (
    <div className="container">
      <h2 className="my-3">Hospital Admission Forecast</h2>

      {/* Dropdown for forecast horizon */}
      <Form.Group className="mb-3">
        <Form.Label>Forecast Horizon</Form.Label>
        <Form.Select
          value={days}
          onChange={(e) => setDays(parseInt(e.target.value))}
        >
          <option value={3}>Next 3 Days</option>
          <option value={7}>Next 7 Days</option>
          <option value={14}>Next 14 Days</option>
          <option value={30}>Next 30 Days</option>
        </Form.Select>
      </Form.Group>

      {loading ? (
        <div className="text-center my-4">
          <Spinner animation="border" />
          <p>Loading forecast...</p>
        </div>
      ) : (
        <>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Date</th>
                <th>Predicted Admissions</th>
              </tr>
            </thead>
            <tbody>
              {forecast.map((f, idx) => (
                <tr key={idx}>
                  <td>{new Date(f.date).toLocaleDateString()}</td>
                  <td>{f.predicted_admissions}</td>
                </tr>
              ))}
            </tbody>
          </Table>

          <h3 className="mt-4">AI Summary</h3>
          <Alert variant="info" style={{ whiteSpace: "pre-line" }}>
            {summary}
          </Alert>
        </>
      )}
    </div>
  );
};

export default Forecast;
