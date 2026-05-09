import httpx
from bs4 import BeautifulSoup

# fetch Page -> parse HTML -> strip junk tags -> return clean plain text

async def scrape_text(url : str):
    #setting user agent to mozilla so websites think that the request is coming from real browser
    header = {
        "User-Agent": "Mozilla/5.0"
    }
    #set header and make the request

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers = header, timeout=10)
        response.raise_for_status()
    #parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    #Remove noise tags
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    #Extract and clean text
    text = soup.get_text(separator=" ", strip=True) #Joins text across HTML tags with a space
    return " ".join(text.split()) #Collapses all messy whitespace into single spaces
 
