import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./StockNews.css";
import Header from "../../components/Header/Header";

function App() {
  const { symbol } = useParams();
  const [news, setNews] = useState([]);
  const [url, setUrl] = useState([]);
  const [latestRange, setLatestRange] = useState("");

  useEffect(() => {
    // Call your Flask backend API
    fetch(`/api/stocks/${symbol}/news`)
      .then((res) => res.json())
      .then((data) => {
        setLatestRange(data.lastUpdated);

        const combinedNews = [...(data.marketauxNews || []), ...(data.finnhubNews || [])];
        setNews(combinedNews);
      });
  }, [symbol]);

  return (
    <div className="news-container">
      <Header />
      {/* <p className="dateRange">
        <i>Last Updated: {latestRange}</i>
      </p> */}

      <div className="news-outer">
        {news.map((article, index) => (
          <div
            className="news-card"
            key={index}
          >
            <h2 className="headline">{article.title || article.headline}</h2>
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                className="image"
                src={article.image_url || article.image || "https://dummyimage.com/600x400/cccccc/000000&text=No+Image"}
                alt={article.title || article.headline}
              ></img>
            </a>
            <p className="overview">{article.description || article.summary || "Article Overview Not Provided"}</p>
            <div className="url">
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                Read Article
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
