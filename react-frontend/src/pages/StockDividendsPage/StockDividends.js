import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./StockDividends.css";
import Header from "../../components/Header/Header";
import { Bar, BarChart, Legend, Text, AreaChart, Area, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

function StockDividends() {
  const { symbol } = useParams();
  const [dividends, setDividends] = useState([]);

  useEffect(() => {
    fetch(`/api/stocks/${symbol}/dividends`)
      .then((res) => res.json())
      .then((data) => {
        setDividends(data.dividends);
      });
  }, [symbol]);

  return (
    <div className="dividends-container">
      <Header />
      <div className="dividends-data-table">
        {dividends === null ? (
          <p>Loading dividend data...</p>
        ) : dividends.length === 0 ? (
          <p className="no-data-msg">No dividend data available for {symbol.toUpperCase()}.</p>
        ) : (
          <>
            <table className="dividends-table">
              <thead>
                <tr>
                  <th>Cash Amount</th>
                  <th>Ex Dividend Date</th>
                  <th>Declaration Date</th>
                  <th>Pay Date</th>
                  <th>Frequency</th>
                </tr>
              </thead>
              <tbody>
                {dividends.map((item, index) => (
                  <tr
                    key={index}
                    className="rows"
                  >
                    <td>${Number(item.cash_amount).toFixed(2)}</td>
                    <td>{item.ex_dividend_date}</td>
                    <td>{new Date(item.declaration_date).toLocaleDateString()}</td>
                    <td>{new Date(item.pay_date).toLocaleDateString()}</td>
                    <td>{item.frequency}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="dividends-mobile-cards">
              {dividends.map((item, index) => (
                <div
                  key={index}
                  className="dividends-mobile-card"
                >
                  <p>
                    <span className="dividends-mobile-label">Cash Amount:</span> ${Number(item.cash_amount).toFixed(2)}
                  </p>
                  <p>
                    <span className="dividends-mobile-label">Ex-Date:</span> {item.ex_dividend_date}
                  </p>
                  <p>
                    <span className="dividends-mobile-label">Declared:</span> {new Date(item.declaration_date).toLocaleDateString()}
                  </p>
                  <p>
                    <span className="dividends-mobile-label">Pay Date:</span> {new Date(item.pay_date).toLocaleDateString()}
                  </p>
                  <p>
                    <span className="dividends-mobile-label">Frequency:</span> {item.frequency}
                  </p>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default StockDividends;
