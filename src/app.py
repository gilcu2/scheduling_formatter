from fastapi import FastAPI
from typing import Dict
from lib import Scheduling, format

app = FastAPI()


@app.get("/hello")
async def hello() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def hello_parameters(name: str, number: int = 0) -> Dict[str, str]:
    return {"message": f"Hello {name}{number}"}


@app.post("/format_scheduling")
async def format_scheduling(scheduling: Scheduling) -> str:
    print(f"scheduling: {scheduling}")
    return f"{format(scheduling)}"
