import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
  setLoading(true);
  setError(null);
  try {
    const res = await fetch("https://cloud-scraper-cbiy.onrender.com/books");
    
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }

    const result = await res.json();
    
    // Ensure data is an array before setting state
    if (!Array.isArray(result)) {  // Check if result is directly the array
      throw new Error("Data is not in expected array format");
    }

    setData(result || []); // Fallback to empty array
  } catch (err) {
    console.error("Fetch error:", err);
    setError(err.message);
    setData([]); // Reset to empty array on error
  } finally {
    setLoading(false);
  }
};

  const handleScrape = async () => {
    setLoading(true);
    setError(null);
    try {
      const scrapeRes = await fetch("https://cloud-scraper-cbiy.onrender.com/scrape");
      if (!scrapeRes.ok) throw new Error("Scraping failed");
      await fetchData();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Cloud Scraper Admin Panel</h1>
      <button onClick={handleScrape} disabled={loading}>
        {loading ? "Scraping..." : "Scrape Now"}
      </button>
      
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <table border="1" cellPadding="10" style={{ marginTop: 20 }}>
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
              <td colSpan="3" style={{ textAlign: "center" }}>
                {loading ? "Loading..." : "No data available"}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}