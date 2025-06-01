// frontend/src/App.js or similar
const BACKEND_URL = "https://cloud-scraper-cbiy.onrender.com"; 

fetch(`${BACKEND_URL}/scrape`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ url: inputUrl }),
})
