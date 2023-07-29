from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
#from fastapi.responses import HTMLResponse
#from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })