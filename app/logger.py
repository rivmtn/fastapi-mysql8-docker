import logging

from starlette.requests import Request
from starlette.types import Message

logger = logging.getLogger("main")
logging.basicConfig(level=logging.DEBUG, encoding='utf-8')
steam_handler = logging.FileHandler('info.log', mode='w', encoding='utf-8')
logger.addHandler(steam_handler)


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}

    request._receive = receive


def log_info(req_headers, req_body, res_status_code, res_headers, res_body):
    logging.info(f">>> REQUEST HEADERS: {req_headers}")
    logging.info(f">>> REQUEST BODY: {req_body.decode('utf-8')}")
    logging.info(f">>> RESPONSE STATUS CODE: {res_status_code}")
    logging.info(f">>> RESPONSE HEADERS: {res_headers}")
    logging.info(f">>> RESPONSE BODY: {res_body.decode('utf-8')}")
