import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./StockFinancials.css";
import Header from "../../components/Header/Header";
import { Bar, BarChart, Legend, Text, AreaChart, Area, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

function StockFinancials() {
  const { symbol } = useParams();
  const [financials, setFinancials] = useState([]);
  const [recentFinancials, setRecentFinancials] = useState([]);

  useEffect(() => {
    fetch(`/api/stocks/${symbol}/financials`)
      .then((res) => res.json())
      .then((data) => {
        setFinancials(data.financial_data);
        const currYear = new Date().getFullYear();
        setRecentFinancials(data.financial_data.filter((item) => item.year >= currYear - 1));
      });
  }, [symbol]);

  return (
    <div className="financials-container">
      <Header />
      <div className="financials-data-table">
        {financials === null ? (
          <p> Loading financial data...</p>
        ) : financials.length === 0 ? (
          <p className="no-data-msg">No financial data available for {symbol.toUpperCase()}.</p>
        ) : (
          <>
            <table className="financials-table">
              <thead>
                <tr>
                  <th>Year</th>
                  <th>Quarter</th>
                  <th>Revenue</th>
                  <th>Net Income</th>
                  <th>Assets</th>
                  <th>Liabilities</th>
                  <th>Equity</th>
                  <th>Cash Flow (Op/Inv/Fin)</th>
                </tr>
              </thead>
              <tbody>
                {financials.map((item, index) => (
                  <tr
                    key={index}
                    className="rows"
                  >
                    <td>{item.year}</td>
                    <td>{item.quarter}</td>
                    <td>${item.revenue.toLocaleString()}</td>
                    <td>${item.net_income.toLocaleString()}</td>
                    <td>${item.assets.toLocaleString()}</td>
                    <td>${item.liabilities.toLocaleString()}</td>
                    <td>${item.equity.toLocaleString()}</td>
                    <td>
                      ${item.operating_cash_flow.toLocaleString()} / ${item.investing_cash_flow.toLocaleString()} / ${item.financing_cash_flow.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="financials-mobile-cards">
              {financials.map((item, index) => (
                <div
                  key={index}
                  className="financials-mobile-card"
                >
                  <p>
                    <span className="financials-mobile-label">Year:</span> {item.year}
                  </p>
                  <p>
                    <span className="financials-mobile-label">Quarter:</span> {item.quarter}
                  </p>
                  <p>
                    <span className="financials-mobile-label">Revenue:</span> ${item.revenue.toLocaleString()}
                  </p>
                  <p>
                    <span className="financials-mobile-label">Net Income:</span> ${item.net_income.toLocaleString()}
                  </p>
                  <p>
                    <span className="financials-mobile-label">Assets:</span> ${item.assets.toLocaleString()}
                  </p>
                  <p>
                    <span className="financials-mobile-label">Liabilities:</span> ${item.liabilities.toLocaleString()}
                  </p>
                  <p>
                    <span className="financials-mobile-label">Equity:</span> ${item.equity.toLocaleString()}
                  </p>
                  <p>
                    <span className="financials-mobile-label">Cash Flow (Op):</span> ${item.operating_cash_flow.toLocaleString()}
                  </p>
                  <p>
                    <span className="financials-mobile-label">Cash Flow (Inv):</span> ${item.investing_cash_flow.toLocaleString()}
                  </p>
                  <p>
                    <span className="financials-mobile-label">Cash Flow (Fin):</span> ${item.financing_cash_flow.toLocaleString()}
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

export default StockFinancials;
