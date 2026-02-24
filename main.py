from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import init_db
from app.core.logging import setup_logging
from app.core.config import config

setup_logging()

app = FastAPI(
    title=config.APP_NAME, 
    description="Raise a digital pet in a virtual world! Feed, play, and care for your pet to keep it happy and healthy.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc")

@app.on_event("startup")
def on_startup():
    init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
@app.get('/meow', response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>Meow Meow Meow Meow Meow Meow Meow Meow Meow Meow Meow Meow</h1>"