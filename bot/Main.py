from aiohttp import web

from ClientsFactory import get_vk_api_client, get_loop, get_aiohttp_client
from Message import Message

CALLBACK = "/callback"

routes = web.RouteTableDef()

vk = get_vk_api_client()
event_loop = get_loop()
client = get_aiohttp_client()


@routes.post('/callback')
async def hello(request):
    data = await request.json()

    if data["type"] == "confirmation":
        return web.Response(text="0d238b23")
    else:
        await Message(vk, event_loop, (await request.json())["object"]["message"]).answer()

        return web.Response(text="ok")


@routes.get("/")
async def index(request):
    return web.Response(text="ok")


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=5050, host="0.0.0.0", loop=event_loop)
