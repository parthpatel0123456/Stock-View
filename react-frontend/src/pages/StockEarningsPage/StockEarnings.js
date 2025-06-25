import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./StockEarnings.css";
import Header from "../../components/Header/Header";

function StockEarnings() {
  const { symbol } = useParams();
  const [financials, setFinancials] = useState([]);

  useEffect(() => {
    fetch(`/api/stocks/${symbol}/earnings`)
      .then((res) => res.json())
      .then((data) => {
        setFinancials(data.financials);
      });
  }, [symbol]);

  return (
    <div className="earnings-container">
      <Header />
      <div className="data-cards"></div>
    </div>
  );
}

export default StockEarnings;
