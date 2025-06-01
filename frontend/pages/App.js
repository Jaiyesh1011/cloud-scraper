import { useEffect, useState } from "react";
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("https://cloud-scraper-cbiy.onrender.com/books");
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      const result = await res.json();
      if (result.status === "success") {
        setData(result.data || []);
      } else {
        throw new Error(result.message || "Failed to fetch data");
      }
    } catch (err) {
      console.error("Fetch error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("https://cloud-scraper-cbiy.onrender.com/scrape");
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      const result = await res.json();
      if (result.status === "success") {
        await fetchData(); // Refresh data after scraping
      } else {
        throw new Error(result.message || "Scraping failed");
      }
    } catch (err) {
      console.error("Scraping error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="container">
      <h1>📚 Cloud Scraper Admin Panel</h1>
      
      <div className="controls">
        <button 
          onClick={handleScrape} 
          disabled={loading}
          className={loading ? "loading" : ""}
        >
          {loading ? "Scraping..." : "Scrape Now"}
        </button>
        {error && <div className="error">{error}</div>}
      </div>

      {loading && !data.length ? (
        <div className="loading-spinner">Loading...</div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Price</th>
              <th>Stock</th>
            </tr>
          </thead>
          <tbody>
            {data.length > 0 ? (
              data.map((item, index) => (
                <tr key={index}>
                  <td>{item.title}</td>
                  <td>{item.price}</td>
                  <td>{item.stock}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3" className="no-data">
                  {error ? "Error loading data" : "No books found"}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;