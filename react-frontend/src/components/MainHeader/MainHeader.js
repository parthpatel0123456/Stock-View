import "./MainHeader.css";
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
      setSelectedTab("Stock View v1");
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
      <div className="centered-title">
        <h1 className="header-title">{selectedTab}</h1>
      </div>
      <p className="header-full-name">
        <i>Market Insights</i>
      </p>
    </div>
  );
}

export default Header;
