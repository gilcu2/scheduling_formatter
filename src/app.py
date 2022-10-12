from fastapi import FastAPI, Request
from typing import Dict, Any, Optional
from scheduling_formatter.week_formatter import format_week, WeekScheduling
from scheduling_formatter.day_formatter import Day_Scheduling
import uvicorn
from pydantic import BaseModel

app = FastAPI()


def default_response(request: Request, full_path: str) -> Dict[str, Any]:
    return {
        "message": "Hello Wolt",
        "full_path": full_path,
        "base_url": request.base_url,
        "client": request.client,
        "headers": request.headers,
        "method": request.method,
        "path_params": request.path_params,
        "query_params": request.query_params,
        "url": request.url,
    }


class WeekSchedulingPydantic(BaseModel):
    monday: Optional[Day_Scheduling] = None
    tuesday: Optional[Day_Scheduling] = None
    wednesday: Optional[Day_Scheduling] = None
    thursday: Optional[Day_Scheduling] = None
    friday: Optional[Day_Scheduling] = None
    saturday: Optional[Day_Scheduling] = None
    sunday: Optional[Day_Scheduling] = None

    def to_WeekScheduling(self) -> WeekScheduling:
        return {}


@app.post("/format_scheduling")
async def format_scheduling(scheduling_pydactic: WeekSchedulingPydantic) -> str:
    return f"{format_week(scheduling_pydactic.to_WeekScheduling()).unwrap()}"


@app.get("/{full_path:path}")
async def any_get(request: Request, full_path: str) -> Dict[str, str]:
    return default_response(request, full_path)


@app.post("/{full_path:path}")
async def any_other_post(request: Request, full_path: str) -> Dict[str, str]:
    return default_response(request, full_path)


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
