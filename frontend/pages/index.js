import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch("https://cloud-scraper-cbiy.onrender.com/books");
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("Failed to fetch data", err);
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async () => {
    setLoading(true);
    try {
      await fetch("https://cloud-scraper-cbiy.onrender.com/scrape");
      await fetchData();
    } catch (err) {
      console.error("Scraping failed", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h1>📚 Cloud Scraper Admin Panel</h1>
      <button onClick={handleScrape} disabled={loading}>
        {loading ? "Scraping..." : "Scrape Now"}
      </button>

      <table border="1" cellPadding="10" style={{ marginTop: 20, width: "100%" }}>
        <thead>
          <tr>
            <th>Title</th>
            <th>Price</th>
            <th>Stock</th>
          </tr>
        </thead>
        <tbody>
          {data.length === 0 && !loading ? (
            <tr>
              <td colSpan="3" style={{ textAlign: "center" }}>No data available</td>
            </tr>
          ) : (
            data.map((item, index) => (
              <tr key={index}>
                <td>{item.title}</td>
                <td>{item.price}</td>
                <td>{item.stock}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
