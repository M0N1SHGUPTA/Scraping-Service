from fastapi import FastAPI
from scraper import scrape_text
from schema import ScrapeRequest

app = FastAPI()

@app.post("/scrape")
def scrape(data: ScrapeRequest):

    text = scrape_text(data.url)

    return {
        "url": data.url,
        "text": text
    }