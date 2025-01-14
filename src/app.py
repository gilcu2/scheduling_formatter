from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from typing import Dict, Any
from scheduling_formatter.week_formatter import format_week, WeekSchedulingPydantic
import uvicorn
import logging

app = FastAPI()


def default_response(request: Request, full_path: str) -> Dict[str, Any]:
    return {
        "message": "Undefined request",
        "full_path": str(full_path),
        "base_url": str(request.base_url),
        "client": str(request.client),
        "headers": str(request.headers),
        "method": str(request.method),
        "path_params": str(request.path_params),
        "query_params": str(request.query_params),
        "url": str(request.url),
    }


@app.post("/format_scheduling", response_class=PlainTextResponse)
def format_scheduling(scheduling_pydantic: WeekSchedulingPydantic) -> str:
    logging.info("/format_scheduling {input}", extra={"input": scheduling_pydantic})
    return format_week(scheduling_pydantic.to_week_scheduling()).unwrap()


@app.get("/{full_path:path}")
def any_get(request: Request, full_path: str) -> Dict[str, str]:
    logging.info("Get {input}", extra={"input": request})
    return default_response(request, full_path)


@app.post("/{full_path:path}")
def any_other_post(request: Request, full_path: str) -> Dict[str, str]:
    logging.info("Post {input}", extra={"input": request})
    return default_response(request, full_path)


if __name__ == "__main__":
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)
