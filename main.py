from fastapi import FastAPI, HTTPException, status
from httpx import HTTPStatusError, ConnectError, TimeoutException
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

    except TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail = "Request Time Out"
        )
    
    except ConnectError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail = "Could not connect to URL"
        )
    
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail = str(e)
        )
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Unexpected Error: {str(e)}")