import os
import requests
from datetime import datetime, timezone
 
 
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
 
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
 
 
def clean_value(value):
 
 
    if value is None or value == "" or value == "None" or value == "-":
        return None
 
    try:
        number = float(value)
 
        if number.is_integer():
            return int(number)
 
        return number
 
    except (ValueError, TypeError):
        return value
 
 
def fetch_alpha_vantage_data(function, ticker):
    """
    Fetch information from Alpha Vantage API.
    """
 
    if not ALPHA_VANTAGE_API_KEY:
        raise ValueError("Alpha Vantage API key is not configured")
 
    params = {
        "function": function,
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
 
    response = requests.get(
        ALPHA_VANTAGE_URL,
        params=params,
        timeout=30
    )
 
    response.raise_for_status()
 
    result = response.json()
 
    if "Error Message" in result:
        raise ValueError(result["Error Message"])
 
    if "Note" in result:
        raise ValueError("Alpha Vantage API rate limit reached: " + result["Note"])
 
    if "Information" in result:
        raise ValueError(result["Information"])
 
    return result
 
 
def get_company_profile(ticker: str):
    """
    Retrieve company profile information using Alpha Vantage.
    """
 
    try:
        result = fetch_alpha_vantage_data(
            "OVERVIEW",
            ticker
        )
 
        if not result or not result.get("Name"):
            return {
                "success": False,
                "message": "Company profile information is unavailable.",
                "data": None
            }
 
        profile = {
            "symbol": result.get("Symbol"),
            "company_name": result.get("Name"),
            "short_name": result.get("Name"),
            "sector": result.get("Sector"),
            "industry": result.get("Industry"),
            "country": result.get("Country"),
            "website": None,
            "business_summary": result.get("Description"),
            "exchange": result.get("Exchange"),
            "currency": result.get("Currency"),
            "employees": clean_value(result.get("FullTimeEmployees")),
            "market_cap": clean_value(result.get("MarketCapitalization")),
            "current_price": None,
            "52_week_high": clean_value(result.get("52WeekHigh")),
            "52_week_low": clean_value(result.get("52WeekLow")),
            "dividend_yield": clean_value(result.get("DividendYield")),
            "pe_ratio": clean_value(result.get("PERatio")),
            "eps": clean_value(result.get("EPS")),
 
            # Additional financial ratios
            "book_value": clean_value(result.get("BookValue")),
            "profit_margin": clean_value(result.get("ProfitMargin")),
            "operating_margin": clean_value(result.get("OperatingMarginTTM")),
            "return_on_assets": clean_value(result.get("ReturnOnAssetsTTM")),
            "return_on_equity": clean_value(result.get("ReturnOnEquityTTM")),
            "revenue_ttm": clean_value(result.get("RevenueTTM")),
            "ebitda": clean_value(result.get("EBITDA")),
            "analyst_target_price": clean_value(result.get("AnalystTargetPrice"))
        }
 
        return {
            "success": True,
            "message": "Company profile retrieved successfully.",
            "data": profile
        }
 
    except Exception as e:
        return {
            "success": False,
            "message": f"Unable to retrieve company profile: {str(e)}",
            "data": None
        }
 
 
def get_financial_statement(ticker: str, statement_type: str):
    """
    Retrieve income statement, balance sheet or cash flow
    using Alpha Vantage.
    """
 
    functions = {
        "income_statement": "INCOME_STATEMENT",
        "balance_sheet": "BALANCE_SHEET",
        "cash_flow": "CASH_FLOW"
    }
 
    if statement_type not in functions:
        return {
            "success": False,
            "message": "Invalid financial statement type.",
            "data": None
        }
 
    try:
        result = fetch_alpha_vantage_data(
            functions[statement_type],
            ticker
        )
 
        annual_reports = result.get("annualReports", [])
        quarterly_reports = result.get("quarterlyReports", [])
 
        if not annual_reports and not quarterly_reports:
            return {
                "success": False,
                "message": f"{statement_type.replace('_', ' ').title()} is unavailable.",
                "data": None
            }
 
        records = {}
 
        # Process annual reports
        for report in annual_reports:
 
            period = report.get("fiscalDateEnding")
 
            if not period:
                continue
 
            period_name = f"{period} (Annual)"
 
            for metric, value in report.items():
 
                if metric in ["fiscalDateEnding", "reportedCurrency"]:
                    continue
 
                if metric not in records:
                    records[metric] = {}
 
                records[metric][period_name] = clean_value(value)
 
        # Process quarterly reports
        for report in quarterly_reports:
 
            period = report.get("fiscalDateEnding")
 
            if not period:
                continue
 
            period_name = f"{period} (Quarterly)"
 
            for metric, value in report.items():
 
                if metric in ["fiscalDateEnding", "reportedCurrency"]:
                    continue
 
                if metric not in records:
                    records[metric] = {}
 
                records[metric][period_name] = clean_value(value)
 
        statement_data = []
 
        for metric, values in records.items():
            statement_data.append({
                "metric": metric,
                "values": values
            })
 
        return {
            "success": True,
            "message": f"{statement_type.replace('_', ' ').title()} retrieved successfully.",
            "total_metrics": len(statement_data),
            "data": statement_data
        }
 
    except Exception as e:
        return {
            "success": False,
            "message": f"Unable to retrieve {statement_type}: {str(e)}",
            "data": None
        }
 
 
def get_company_financial_information(ticker: str):
    """
    Retrieve company profile and financial statements.
    """
 
    try:
 
        profile = get_company_profile(ticker)
 
        income_statement = get_financial_statement(
            ticker,
            "income_statement"
        )
 
        balance_sheet = get_financial_statement(
            ticker,
            "balance_sheet"
        )
 
        cash_flow = get_financial_statement(
            ticker,
            "cash_flow"
        )
 
        return {
            "success": True,
            "ticker": ticker.upper(),
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
 
            "company_profile": profile,
 
            "financial_statements": {
                "income_statement": income_statement,
                "balance_sheet": balance_sheet,
                "cash_flow_statement": cash_flow
            }
        }
 
    except Exception as e:
        return {
            "success": False,
            "ticker": ticker.upper(),
            "message": (
                "Unable to retrieve company financial information: "
                + str(e)
            ),
            "data": None
        }
 