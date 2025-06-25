import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Text, AreaChart, Area, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import "./StockOverviewPage.css";
import Header from "../../components/Header/Header";

function StockOverviewPage() {
  const { symbol } = useParams();
  const [chartData, setChartData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChartData = async () => {
      const API_KEY = process.env.REACT_APP_POLYGON_API_KEY;

      const now = new Date();
      const oneMonthAgo = new Date();
      oneMonthAgo.setDate(now.getDate() - 30);

      const formatDate = (d) => d.toISOString().split("T")[0]; // YYYY-MM-DD

      const from = formatDate(oneMonthAgo);
      const to = formatDate(now);

      const url = `https://api.polygon.io/v2/aggs/ticker/${symbol}/range/1/day/${from}/${to}?adjusted=true&sort=asc&apiKey=${API_KEY}`;

      try {
        const res = await fetch(url);
        const data = await res.json();

        if (!data.results || data.results.length === 0) {
          setError("No chart data available.");
          return;
        }

        const formatted = data.results.map((item) => ({
          date: new Date(item.t).toLocaleDateString(),
          close: item.c,
        }));

        setChartData(formatted);
      } catch (err) {
        setError("Error fetching chart data.");
        console.error(err);
      }
    };

    fetchChartData();
  }, [symbol]);

  return (
    <div className="overview-container">
      <Header />
      {error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <ResponsiveContainer
          className="responsive-container"
          width="100%"
          height={500}
        >
          <AreaChart
            className="line-container"
            data={chartData}
            margin={{ top: 5, right: 50, left: 20, bottom: 5 }}
          >
            <defs>
              <linearGradient
                id="colorUv"
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop
                  offset="5%"
                  stopColor="#007bff"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="#007bff"
                  stopOpacity={0}
                />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#ccc" />
            <XAxis
              dataKey="date"
              padding={{ left: 0, right: 0 }}
              tickFormatter={(dateStr) => {
                const date = new Date(dateStr);
                const options = { month: "short", day: "numeric" };
                return date.toLocaleDateString(undefined, options);
              }}
            />
            <YAxis
              domain={["auto", "auto"]}
              padding={{ top: 25, bottom: 25 }}
            />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="close"
              stroke="#007bff"
              fillOpacity={1}
              fill="url(#colorUv)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

export default StockOverviewPage;
