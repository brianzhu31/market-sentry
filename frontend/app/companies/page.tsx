"use client";

import { useState, useEffect } from "react";
import { CompanyFull } from "@/types";
import { CompaniesTable } from "./components/companies-table";
import { fetchAllCompaniesWithScore } from "./actions/fetch-companies";

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<CompanyFull[]>([]);

  useEffect(() => {
    const getAllCompanies = async () => {
      const fetchAllCompaniesWithScoreResponse = await fetchAllCompaniesWithScore();
      if (fetchAllCompaniesWithScoreResponse.data) {
        setCompanies(fetchAllCompaniesWithScoreResponse.data);
      }
    };
    getAllCompanies();
  }, []);

  if (companies.length === 0) {
    return <></>
  }

  return (
    <div className="flex flex-col justify-center items-center min-h-screen">
      <div className="p-16">
        <p className="text-3xl md:text-4xl lg:text-5xl font-bold">All Companies</p>
      </div>
      <div className="w-full max-w-[1500px] px-8">
        <CompaniesTable companies={companies} setCompanies={setCompanies} />
      </div>
    </div>
  );
}
