"""
LangChain Tools for pitch deck verification agents
"""
from langchain_core.tools import Tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import json


class VerificationTools:
    """Collection of tools for pitch deck verification"""

    def __init__(self):
        self.search = DuckDuckGoSearchAPIWrapper()

    def web_search(self, query: str) -> str:
        """
        Search the web for information to verify claims.
        Useful for finding recent news, market data, and company information.
        """
        try:
            results = self.search.run(query)
            return results
        except Exception as e:
            return f"Search failed: {str(e)}"

    def search_company_info(self, company_name: str) -> str:
        """
        Search for company information including funding, team, and metrics.
        Useful for verifying company-specific claims.
        """
        query = f"{company_name} funding crunchbase startup"
        try:
            results = self.search.run(query)
            return f"Company Information for {company_name}:\n{results}"
        except Exception as e:
            return f"Company search failed: {str(e)}"

    def search_market_data(self, market_query: str) -> str:
        """
        Search for market size, growth rates, and industry statistics.
        Useful for verifying market-related claims.
        """
        query = f"{market_query} market size TAM SAM statistics gartner statista"
        try:
            results = self.search.run(query)
            return f"Market Data:\n{results}"
        except Exception as e:
            return f"Market search failed: {str(e)}"

    def search_person(self, person_name: str, company: str = "") -> str:
        """
        Search for person's background and credentials.
        Useful for verifying team member claims.
        """
        query = f"{person_name} {company} linkedin background experience"
        try:
            results = self.search.run(query)
            return f"Person Information for {person_name}:\n{results}"
        except Exception as e:
            return f"Person search failed: {str(e)}"

    def search_technology(self, technology_claim: str) -> str:
        """
        Search for technology benchmarks and industry standards.
        Useful for verifying technical performance claims.
        """
        query = f"{technology_claim} benchmark industry standard performance"
        try:
            results = self.search.run(query)
            return f"Technology Benchmarks:\n{results}"
        except Exception as e:
            return f"Technology search failed: {str(e)}"

    def analyze_competitor(self, competitor_name: str, sector: str = "") -> str:
        """
        Search for competitor information and market positioning.
        Useful for competitive analysis and validation.
        """
        query = f"{competitor_name} {sector} revenue funding market share"
        try:
            results = self.search.run(query)
            return f"Competitor Analysis for {competitor_name}:\n{results}"
        except Exception as e:
            return f"Competitor search failed: {str(e)}"

    def get_tools(self) -> List[Tool]:
        """Return list of LangChain tools"""
        return [
            Tool(
                name="web_search",
                func=self.web_search,
                description="Search the web for general information. Input should be a search query string."
            ),
            Tool(
                name="search_company_info",
                func=self.search_company_info,
                description="Search for company information including funding, team, and metrics. Input should be the company name."
            ),
            Tool(
                name="search_market_data",
                func=self.search_market_data,
                description="Search for market size, growth rates, and industry statistics. Input should be a market-related query."
            ),
            Tool(
                name="search_person",
                func=self.search_person,
                description="Search for a person's background and credentials. Input should be the person's name."
            ),
            Tool(
                name="search_technology",
                func=self.search_technology,
                description="Search for technology benchmarks and industry standards. Input should be a technology claim."
            ),
            Tool(
                name="analyze_competitor",
                func=self.analyze_competitor,
                description="Search for competitor information and market positioning. Input should be the competitor name."
            )
        ]
