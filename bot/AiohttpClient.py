from asyncio import get_event_loop

import aiohttp
from aiohttp import ClientSession


class AIOHTTPClient:
    def __init__(
            self,
            session=None,
            loop=None,
            verify_ssl: bool = False,
            trust_env: bool = False,
    ):
        self.loop = loop or get_event_loop()
        self.session = session or ClientSession(
            loop=self.loop,
            connector=aiohttp.TCPConnector(verify_ssl=verify_ssl),
            trust_env=trust_env,
        )

    async def close(self):
        await self.session.close()

    async def request_text(self, method: str, url: str, data=None) -> str:
        data = data or {}

        async with self.session.request(method, url, data=data) as resp:
            return await resp.text()

    async def request_json(self, method: str, url: str, data=None) -> dict:
        data = data or {}

        async with self.session.request(method, url, data=data) as resp:
            return await resp.json()

    async def request_send_json(self, method: str, url: str, json=None) -> dict:
        json = json or {}
        async with self.session.request(method, url, json=json) as resp:
            return await resp.json()
