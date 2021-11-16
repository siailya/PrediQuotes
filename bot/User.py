import asyncio
from datetime import datetime

from vkwave_api import API


class User:
    def __init__(self, api, id):
        self._id = id
        self._api = api
        self.first_name = None
        self.last_name = None
        self.full_name = None
        self.photo_200 = None

    def set_id(self, new_id):
        self._id = new_id

    async def get_name(self):
        if self.first_name is None:
            data = (await self._api.users.get(user_ids=self._id)).response[0]

            self.first_name = data.first_name
            self.last_name = data.last_name
            self.full_name = data.first_name + " " + data.last_name

        return {"full_name": self.full_name,
                "first_name": self.first_name,
                "last_name": self.last_name}

    async def get_photo_url(self, size: str = "max"):
        if getattr(self, "photo_" + size, None) is None:
            data = (await self._api.users.get(user_ids=self._id, fields=["photo_" + size])).response[0]
            setattr(self, "photo_" + size, getattr(data, "photo_" + size))

        return getattr(self, "photo_" + size)
