import React, { useEffect, useState, useContext } from "react";
import logo from "./logo.svg";
import "./App.css";
import { useNavigate } from "react-router-dom";
import { CompanyContext } from "./context/CompanyContext";
import MainHeader from "./components/MainHeader/MainHeader";

const FinnhubSearch = () => {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [selectedStockIndex, setSelectedStockIndex] = useState(0);
  const [selectedStock, setSelectedStock] = useState("");
  const apiKey = process.env.REACT_APP_FINNHUB_API_KEY;
  const { setCompanyName } = useContext(CompanyContext);

  const navigate = useNavigate();

  // --- FUTURE AUTOFILLER ---
  // useEffect(() => {
  //   const params = new URLSearchParams(window.location.search);
  //   const q = params.get("q");
  //   if (q) setQuery(q);
  // }, []);

  useEffect(() => {
    if (query.length === 0) {
      setSuggestions([]);
      return;
    }
    if (query.length < 2) return;

    const timeoutId = setTimeout(() => {
      fetch(`https://finnhub.io/api/v1/search?q=${query}&token=${apiKey}`)
        .then((res) => res.json())
        .then((data) => setSuggestions(data.result || []));
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [query]);

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      setSelectedStockIndex((prev) => (prev + 1) % suggestions.length);
    } else if (e.key === "ArrowUp") {
      setSelectedStockIndex((prev) => (prev - 1 + suggestions.length) % suggestions.length);
    } else if (e.key === "Enter") {
      const selectedItem = suggestions[selectedStockIndex];
      setSelectedStock(selectedItem.displaySymbol);
      setSuggestions([]);
      setCompanyName(selectedItem.description);

      navigate(`/stocks/${selectedItem.displaySymbol}`);
    }
  };

  const handleClick = (item) => {
    setSelectedStock(item.displaySymbol);
    setSuggestions([]);
    setCompanyName(item.description);
    navigate(`/stocks/${item.displaySymbol}`);
  };

  return (
    <div class="search-box-container">
      <input
        className="search-box"
        type="text"
        placeholder="Search a stock..."
        value={query.toUpperCase()}
        onChange={(e) => {
          setQuery(e.target.value);
          setSelectedStockIndex(0);
        }}
        onKeyDown={handleKeyDown}
      />
      <ul className="suggestions">
        {suggestions.map((item, index) => (
          <li
            className="suggested-stock"
            key={item.symbol}
            onClick={() => handleClick(item)}
            style={{
              padding: "5px 10px",
              cursor: "pointer",
              backgroundColor: index === selectedStockIndex ? "#d0ebff" : "transparent",
            }}
          >
            {item.description} ({item.displaySymbol})
          </li>
        ))}
      </ul>
    </div>
  );
};

function App() {
  return (
    <div className="stock-container">
      <div className="main-content">
        <div className="main-header">
          <MainHeader />
        </div>
        <div className="search">
          <FinnhubSearch />
        </div>
        <hr className="stock-container-line" />
        <div className="details-container">
          <div className="tech-stack-container">
            <h2 className="title">Tech Stack</h2>
            <div className="tech-stack-wrapper">
              <div className="tech-stack-cards">
                <div className="tech-stack-card">
                  <h3 className="tech-stack-sub-headline">Frontend</h3>
                  <ul className="list-overview">
                    <li className="list">React (v1)</li>
                    <li className="list">JavaScript (v1)</li>
                    <li className="list">HTML (v1)</li>
                    <li className="list">CSS (v1)</li>
                  </ul>
                </div>
                <div className="tech-stack-card">
                  <h3 className="tech-stack-sub-headline">Backend</h3>
                  <ul className="list-overview">
                    <li className="list">Python Flask (v1)</li>
                  </ul>
                </div>
                <div className="tech-stack-card">
                  <h3 className="tech-stack-sub-headline">APIs</h3>
                  <ul className="list-overview">
                    <li className="list">Alpha Vantage (v1)</li>
                    <li className="list">Polygon.io (v1)</li>
                    <li className="list">Finnhub (v1)</li>
                    <li className="list">MarketAux (v1)</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <hr className="stock-container-line" />
          <div className="features-container">
            <h2 className="title">Features</h2>
            <div className="list-container">
              <ul className="list-overview">
                <li className="list">Stock Overview (v1)</li>
                <li className="list">AI Chat (v2)</li>
                <li className="list">News Feed (v1)</li>
                <li className="list">Earnings Data (v2)</li>
                <li className="list">Financial Data (v1)</li>
                <li className="list">Dividends Data (v1)</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
