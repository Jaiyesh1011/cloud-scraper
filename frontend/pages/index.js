import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const BACKEND_URL = "https://cloud-scraper-cbiy.onrender.com"; // Confirm this is your backend URL

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${BACKEND_URL}/books`);
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);

      const result = await res.json();
      if (result.status !== "success") throw new Error(result.message || "Invalid response");

      setData(Array.isArray(result.data) ? result.data : []);
    } catch (err) {
      setError(err.message);
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async () => {
    setLoading(true);
    setError(null);
    try {
      const scrapeRes = await fetch(`${BACKEND_URL}/scrape`);
      if (!scrapeRes.ok) {
        const errRes = await scrapeRes.json().catch(() => null);
        throw new Error(errRes?.message || "Scraping failed");
      }
      // Scrape successful, fetch updated data
      await fetchData();
    } catch (err) {
      setError(err.message);
      setLoading(false); // Stop loading on error
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div style={{ padding: 20, maxWidth: 1000, margin: "auto", backgroundColor: "#fff", borderRadius: 8, boxShadow: "0 2px 10px rgba(0,0,0,0.1)" }}>
      <h1 style={{ color: "#2c3e50", textAlign: "center" }}>Cloud Scraper Admin Panel</h1>
      <div style={{ margin: "20px 0", display: "flex", justifyContent: "center" }}>
        <button onClick={handleScrape} disabled={loading}>
          {loading ? "Scraping..." : "Scrape Now"}
        </button>
      </div>

      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      <table border="1" cellPadding="10" style={{ width: "100%", borderCollapse: "collapse", marginTop: 20 }}>
        <thead>
          <tr style={{ backgroundColor: "#f2f2f2", fontWeight: "bold" }}>
            <th>Title</th>
            <th>Price</th>
            <th>Stock</th>
          </tr>
        </thead>
        <tbody>
          {loading && data.length === 0 ? (
            <tr>
              <td colSpan="3" style={{ textAlign: "center" }}>Loading...</td>
            </tr>
          ) : Array.isArray(data) && data.length > 0 ? (
            data.map((item, idx) => (
              <tr key={idx}>
                <td>{item.title}</td>
                <td>{item.price}</td>
                <td>{item.stock}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3" style={{ textAlign: "center" }}>No data available</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
