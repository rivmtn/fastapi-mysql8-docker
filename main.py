import os
import sys
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, APIRouter, Response, Request
from fastapi_sqlalchemy import DBSessionMiddleware
from pytz import timezone
from starlette.background import BackgroundTask
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from app.database import init_db
from app.env import DB_URL
from app.logger import set_body, log_info

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))

router = APIRouter()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DBSessionMiddleware, db_url=DB_URL)
app.include_router(router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def home():
    return HTMLResponse(content=f"""
<body>
<div style="width: 400px; margin: 50 auto;">
    <h1> 현재 서버 구동 중입니다.</h1>
    <h2>{datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")}</h2>
</div>
</body>
""")


@app.post("/")
async def post_test(data: Dict[Any, Any]):
    return data


@app.middleware('http')
async def some_middleware(request: Request, call_next):
    req_headers = request.headers
    req_body = await request.body()
    await set_body(request, req_body)
    response = await call_next(request)
    res_headers = response.headers
    res_status_code = response.status_code
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    task = BackgroundTask(log_info, req_headers, req_body, res_status_code, res_headers, res_body)
    return Response(content=res_body, status_code=response.status_code,
                    headers=dict(response.headers), media_type=response.media_type, background=task)

