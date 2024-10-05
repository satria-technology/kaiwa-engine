from interfaces.fastapi import twilio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Kaiwa Engine - Satria Technology",
    description="The API for Kaiwa Engine",
    version="1.0.0",
    servers=[
        {"url": "https://54pzhk5t-8000.asse.devtunnels.ms", "description": "Local development server"},
        {"url": "https://kaiwa-engine.satria.technology", "description": "Production server"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return "✩░▒▓▆▅▃▂▁𝐬𝐚𝐭𝐫𝐢𝐚.𝐭𝐞𝐜𝐡𝐧𝐨𝐥𝐨𝐠𝐲▁▂▃▅▆▓▒░✩"


app.include_router(twilio.router)
