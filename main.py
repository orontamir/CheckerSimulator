import asyncio

from aiohttp import ClientSession
from quart import Quart, request

app = Quart(__name__)
client = None


async def add_request(delay: float, url: str, method: str, body: str, ):
    global client
    await asyncio.sleep(delay)
    if not client:
        client = ClientSession()
    await client.post(method, url, data=body)


@app.route("/")
async def keepalive():
    return ""


@app.route("/delay_request", methods=["POST"])
async def delay_request():
    request_json = await request.get_json()
    delay = request_json["delay"]
    url = request_json["url"]
    body = request_json["body"]
    method = request_json["method"]
    asyncio.get_event_loop().create_task(add_request(delay, url, method, body))
    return ""


if __name__ == '__main__':
    app.run(host="0.0.0.0")
