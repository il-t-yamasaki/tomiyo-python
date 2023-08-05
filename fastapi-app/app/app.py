from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
#from fastapi.responses import HTMLResponse
#from fastapi.staticfiles import StaticFiles

from src.scrap import scraper
import database.handler_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")

@app.get(path="/api/users")
async def get_list_user():
    result = handler_db.select_all_user()
    return {
        "status": "OK",
        "data": result
    }

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