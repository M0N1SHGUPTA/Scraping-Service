from fastapi import FastAPI, HTTPException, status, Request
from httpx import HTTPStatusError, ConnectError, TimeoutException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from scraper import scrape_text
from schema import ScrapeRequest

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/scrape")
@limiter.limit("5/minute")
async def scrape(request: Request, data: ScrapeRequest):
    try:
        text = await scrape_text(str(data.url))
        return {
            "url": str(data.url),
            "text": text
        }
    except TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request Time Out"
        )
    except ConnectError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Could not connect to URL"
        )
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected Error: {str(e)}"
        )