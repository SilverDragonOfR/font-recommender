import json
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from recommendation import recommend_ranks

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

with open("./data/fonts.json", "r") as file:
    fonts_data = json.load(file)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "fonts": fonts_data})

@app.post("/search", response_class=HTMLResponse)
async def search_font(request: Request, query: str = Form(...)):
    ranked_fonts = recommend_ranks(query)
    return templates.TemplateResponse("index.html", {"request": request, "fonts": {font["name"]: font["details"] for font in ranked_fonts}, "query": query})