from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
#from fastapi.responses import HTMLResponse
#from fastapi.staticfiles import StaticFiles

from src.scrap import scraper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")


@app.get("/search/")
async def search(request: Request, URL: str, keyword: str):
    body_href = None
    if "http" in URL:
        body_href = scraper(URL, keyword)
    return templates.TemplateResponse(
        "search.html", 
        {
            "request": request,
            "result": body_href
        }
    )