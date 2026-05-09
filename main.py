from fastapi import FastAPI, HTTPException, status
from requests.exceptions import HTTPError, ConnectionError, Timeout
from scraper import scrape_text
from schema import ScrapeRequest

app = FastAPI()

@app.post("/scrape")
async def scrape(data: ScrapeRequest):

    try:
        text = await scrape_text(str(data.url))
        return {
            "url": str(data.url),
            "text": text
        }

    except Timeout:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail = "Request Time Out"
        )
    
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail = "Could not connect to URL"
        )
    
    except HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail = str(e)
        )
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Unexpected Error: {str(e)}")