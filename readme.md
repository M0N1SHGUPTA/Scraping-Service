# Scraping-Service

A simple REST API that scrapes and returns clean text from any webpage.

## Stack
- FastAPI
- httpx (async HTTP)
- BeautifulSoup4
- Docker

## Run locally

```bash
git clone https://github.com/M0N1SHGUPTA/Scraping-Service
cd Scraping-Service
pip install -r requirements.txt
uvicorn main:app --reload
```

## Run with Docker

```bash
docker build -t scraper-service .
docker run -p 8000:8000 scraper-service
```

## Usage

```bash
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Response:
```json
{
  "url": "https://example.com",
  "text": "cleaned page text here..."
}
```

## Notes
- Rate limited to 5 requests/minute per IP
- Handles static sites well, JS-heavy sites may need Playwright mode
