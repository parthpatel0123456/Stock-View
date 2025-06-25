import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "../App";
import StockNews from "../pages/StockNewsPage/StockNews";
import StockOverviewPage from "../pages/StockOverviewPage/StockOverviewPage";
import StockEarnings from "../pages/StockEarningsPage/StockEarnings";
import StockFinancials from "../pages/StockFinancialsPage/StockFinancials";
import StockDividends from "../pages/StockDividendsPage/StockDividends";

const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={<Home />}
        />
        <Route
          path="/stocks/:symbol"
          element={<StockOverviewPage />}
        />
        <Route
          path="/stocks/:symbol/news"
          element={<StockNews />}
        />
        <Route
          path="/stocks/:symbol/earnings"
          element={<StockEarnings />}
        />
        <Route
          path="/stocks/:symbol/financials"
          element={<StockFinancials />}
        />
        <Route
          path="/stocks/:symbol/dividends"
          element={<StockDividends />}
        />
      </Routes>
    </Router>
  );
};

export default AppRouter;
