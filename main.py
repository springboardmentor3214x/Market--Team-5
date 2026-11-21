from fastapi import HTTPException
from company_financials import get_company_financial_information
# COMPANY FINANCIAL INFORMATION API
 
@app.get("/financials/{ticker}")
def company_financials(ticker: str):
 
    if not ticker.strip():
        raise HTTPException(
            status_code=400,
            detail="Ticker cannot be empty."
        )
 
    try:
        result = get_company_financial_information(ticker.strip())
 
        if not result.get("success"):
            raise HTTPException(
                status_code=404,
                detail=result.get(
                    "message",
                    "Unable to retrieve company financial information."
                )
            )
 
        return result
 
    except HTTPException:
        raise
 
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve financial information: {str(e)}"
        )