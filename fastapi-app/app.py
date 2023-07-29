from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
#from fastapi.responses import HTMLResponse
#from fastapi.staticfiles import StaticFiles

from src.model import Item


app = FastAPI()
templates = Jinja2Templates(directory='templates')

# 初期リスト
User_list = [
    {"ID":"001","Name":"aaa","Class":"A"},
    {"ID":"002","Name":"bbb","Class":"B"},
]

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "user_list": User_list
        }
    )

# curl -X POST -H "accept: application/json" -H "Content-Type: application/json"
# -d "{\"ID\":\"003\", \"Name\":\"ccc\", \"Class\":\"C\"} " http://127.0.0.1:80/users/
@app.post("/users/")
async def users(user: Item):
    User_list.append({"ID": user.ID,"Name":user.Name,"Class":user.Class})
    return User_list