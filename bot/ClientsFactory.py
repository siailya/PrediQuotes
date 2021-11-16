import asyncio
import os

from vkwave_api import API

from AiohttpClient import AIOHTTPClient

vk = None
client = None
event_loop = None


def get_aiohttp_client():
    global client

    if not client:
        client = AIOHTTPClient()
    return client


def get_vk_api_client():
    global vk, api

    if not vk:
        api = API(os.environ['VKAPI'])
        vk = api.get_api()

    return vk


def get_loop():
    global event_loop

    if not event_loop:
        event_loop = asyncio.get_event_loop()

    return event_loop
