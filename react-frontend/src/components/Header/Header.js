import "./Header.css";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect, useContext } from "react";
import { CompanyContext } from "../../context/CompanyContext";

function Header() {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const [selectedTab, setSelectedTab] = useState("Overview");
  const location = useLocation();
  const { companyName } = useContext(CompanyContext);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (location.pathname.endsWith("/")) {
      setSelectedTab("Stock View");
    } else if (location.pathname.endsWith("/news")) {
      setSelectedTab("News");
    } else if (location.pathname.endsWith("/earnings")) {
      setSelectedTab("Earnings");
    } else if (location.pathname.endsWith("/financials")) {
      setSelectedTab("Financials");
    } else if (location.pathname.endsWith("/dividends")) {
      setSelectedTab("Dividends");
    } else {
      setSelectedTab("Overview");
    }
  }, [location.pathname]);

  return (
    <div className="header-options">
      <div className="top-row">
        <h1 className="header-title">
          {symbol} {selectedTab}
        </h1>
        <div
          className="hamburger"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <div></div>
          <div></div>
          <div></div>
        </div>
        <div className={`buttons-container ${menuOpen ? "active" : ""}`}>
          {menuOpen && (
            <button
              className="close-menu"
              onClick={() => setMenuOpen(false)}
              aria-label="Close menu"
            >
              ✕
            </button>
          )}
          <div className="menu-separator"></div>
          <button
            className="header-buttons"
            onClick={() => navigate(`/`)}
          >
            Home
          </button>
          <button
            className="header-buttons"
            onClick={() => navigate(`/stocks/${symbol}`)}
          >
            AI Chat
          </button>
          <button
            className="header-buttons"
            onClick={() => navigate(`/stocks/${symbol}`)}
          >
            Overview
          </button>
          <button
            className="header-buttons"
            onClick={() => navigate(`/stocks/${symbol}/news`)}
          >
            News
          </button>
          <button
            className="header-buttons"
            onClick={() => navigate(`/stocks/${symbol}/earnings`)}
          >
            Earnings
          </button>
          <button
            className="header-buttons"
            onClick={() => navigate(`/stocks/${symbol}/financials`)}
          >
            Financials
          </button>
          <button
            className="header-buttons"
            onClick={() => navigate(`/stocks/${symbol}/dividends`)}
          >
            Dividends
          </button>
        </div>
      </div>
      <p className="header-full-name">
        <i>{companyName}</i>
      </p>
    </div>
  );
}

export default Header;
