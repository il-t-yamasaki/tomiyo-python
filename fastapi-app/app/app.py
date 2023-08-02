from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
#from fastapi.responses import HTMLResponse
#from fastapi.staticfiles import StaticFiles

from src.model import Item
from bs4 import BeautifulSoup
import urllib.request
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")

# 初期リスト
User_list = [
    {"ID":"001","Name":"aaa","Class":"A"},
    {"ID":"002","Name":"bbb","Class":"B"},
]

@app.get("/users/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "user_list": User_list
        }
    )

# curl -X POST -H "accept: application/json" -H "Content-Type: application/json"
# -d "{\"ID\":\"003\", \"Name\":\"ccc\", \"Class\":\"C\"} " http://127.0.0.1:80/
@app.post("/")
async def users(user: Item):
    User_list.append({"ID": user.ID,"Name":user.Name,"Class":user.Class})
    return User_list



# スクレイピング処理べた書き
#対象のサイトURL
url = "https://www.2ch.sc/bbsmenu.html"

#URLリソースを開く
res = urllib.request.urlopen(url)

#インスタンスの作成
soup = BeautifulSoup(res, 'html5lib')

#head内のタイトルタグを取得
site_title = soup.html.head.title
# print(site_title.string)


#「ニュース」を含むaタグ全部
body_href = soup.find_all("b", text=re.compile(""))
# print(body_href)
#[<a href="http://ai.2ch.sc/newsalpha/">ニュース速報α</a>, <a href="http://ai.2ch.sc/newsalpha/">ニュース速報α</a>,...]


@app.get("/search/")
async def search(request: Request):
    return templates.TemplateResponse(
        "search.html", 
        {
            "request": request,
            "result": body_href
        }
    )