import { useEffect, useState } from "react";

function App() {
  const [events, setEvents] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [eventsResponse, incidentsResponse] = await Promise.all([
          fetch("http://localhost:8080/api/events"),
          fetch("http://localhost:8080/api/incidents"),
        ]);

        if (!eventsResponse.ok || !incidentsResponse.ok) {
          throw new Error("Failed to fetch data from backend");
        }

        const eventsData = await eventsResponse.json();
        const incidentsData = await incidentsResponse.json();

        setEvents(eventsData);
        setIncidents(incidentsData);
      } catch (err) {
        setError("Unable to connect to EventMap backend.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const highSeverityIncidents = incidents.filter(
    (incident) =>
      incident.severity === "HIGH" ||
      incident.severity === "CRITICAL"
  );

  if (loading) {
    return <h2>Loading EventMap...</h2>;
  }

  return (
    <div>
      <h1>EventMap</h1>
      <p>Incident Cause Detection</p>

      <hr />

      {error && <p>{error}</p>}

      <h2>Operational Dashboard</h2>

      <div>
        <h3>Total Events</h3>
        <p>{events.length}</p>
      </div>

      <div>
        <h3>Total Incidents</h3>
        <p>{incidents.length}</p>
      </div>

      <div>
        <h3>High/Critical Incidents</h3>
        <p>{highSeverityIncidents.length}</p>
      </div>

      <hr />

      <h2>Recent Incidents</h2>

      {incidents.length === 0 ? (
        <p>No incidents found.</p>
      ) : (
        incidents.map((incident) => (
          <div key={incident.id}>
            <h3>{incident.title}</h3>
            <p>{incident.description}</p>
            <p>Severity: {incident.severity}</p>
            <p>Status: {incident.status}</p>
            <p>Reported By: {incident.reportedBy}</p>
            <hr />
          </div>
        ))
      )}

      <h2>Recent Events</h2>

      {events.length === 0 ? (
        <p>No events found.</p>
      ) : (
        events.map((event) => (
          <div key={event.id}>
            <h3>{event.serviceName}</h3>
            <p>Type: {event.eventType}</p>
            <p>Severity: {event.severity}</p>
            <p>{event.message}</p>
            <p>Status: {event.status}</p>
            <hr />
          </div>
        ))
      )}
    </div>
  );
}

export default App;