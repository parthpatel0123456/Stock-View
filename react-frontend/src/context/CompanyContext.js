import { createContext, useState, useEffect } from "react";

export const CompanyContext = createContext();

export const CompanyProvider = ({ children }) => {
  const [companyName, setCompanyName] = useState(() => {
    // Initialize from localStorage if exists
    return localStorage.getItem("companyName") || "";
  });

  useEffect(() => {
    // Save to localStorage whenever companyName changes
    localStorage.setItem("companyName", companyName);
  }, [companyName]);

  return <CompanyContext.Provider value={{ companyName, setCompanyName }}>{children}</CompanyContext.Provider>;
};
