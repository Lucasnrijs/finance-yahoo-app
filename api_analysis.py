import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-popular-watchlists"

headers = {
    "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com",
    "x-rapidapi-key": "48a2b57d07mshc303b2f74b3c0c0p1996b8jsnfe9e45101fa7"
}

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    #print(data)
else:
    print(f"Request failed with status code: {response.status_code}")
    # Import FastAPI and necessary components
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/popular-watchlists")
async def get_popular_watchlists():
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=f"API request failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Note: To run this FastAPI app, you'll need to use an ASGI server like uvicorn
    # Run with: uvicorn api_analysis:app --reload
@app.get("/earnings")
async def get_earnings():
    try:
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-earnings"
        
        headers = {
            "x-rapidapi-key": "48a2b57d07mshc303b2f74b3c0c0p1996b8jsnfe9e45101fa7",
            "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }
        
        params = {
            "region": "US",
            "size": "10"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=f"API request failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/market-movers")
async def get_market_movers():
    try:
        movers_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-movers"
        params = {
            "region": "US",
            "lang": "en-US",
            "start": "0",
            "count": "6"
        }
        response = requests.get(movers_url, headers=headers, params=params)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=f"API request failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock-analysis-US/{symbol}")
async def get_stock_analysis(symbol: str):
    try:
        analysis_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"
        params = {
            "symbol": symbol,
            "region": "US"
        }
        response = requests.get(analysis_url, headers=headers, params=params)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=f"API request failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock-analysis-EU/{symbol}")
async def get_stock_analysis_EU(symbol: str):
    try:
        analysis_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"
        params = {
            "symbol": symbol,
            "region": "EU"
        }
        response = requests.get(analysis_url, headers=headers, params=params)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=f"API request failed")
    except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock-analysis-UK/{symbol}")
async def get_stock_analysis_UK(symbol: str):
    try:
        analysis_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"
        params = {
            "symbol": symbol,
            "region": "UK"
        }
        response = requests.get(analysis_url, headers=headers, params=params)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=f"API request failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@app.get("/analysts-saying-US/{symbols}")
async def get_analysts_saying(symbols: str):
    try:
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-what-analysts-are-saying"
        params = {
            "symbols": symbols,
            "region": "US",
            "lang": "en-US"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=f"API request failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysts-saying-EU/{symbols}")
async def get_analysts_saying_EU(symbols: str):
    try:
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-what-analysts-are-saying"
        params = {
            "symbols": symbols,
            "region": "EU",
            "lang": "en-US"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=f"API request failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



