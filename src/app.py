from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from typing import Dict, Any, Optional, cast
from scheduling_formatter.week_formatter import format_week, WeekScheduling
from scheduling_formatter.day_formatter import Day_Scheduling
import uvicorn
from pydantic import BaseModel
import logging

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

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

    def to_week_scheduling(self) -> WeekScheduling:
        return cast(WeekScheduling, self.dict())


@app.post("/format_scheduling", response_class=PlainTextResponse)
def format_scheduling(scheduling_pydantic: WeekSchedulingPydantic) -> str:
    logger.info("/format_scheduling {input}", extra={"input": scheduling_pydantic})
    return format_week(scheduling_pydantic.to_week_scheduling()).unwrap()


@app.get("/{full_path:path}")
def any_get(request: Request, full_path: str) -> Dict[str, str]:
    logger.info("Get {input}", extra={"input": request})
    return default_response(request, full_path)


@app.post("/{full_path:path}")
def any_other_post(request: Request, full_path: str) -> Dict[str, str]:
    logger.info("Post {input}", extra={"input": request})
    return default_response(request, full_path)


if __name__ == "__main__":
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)
