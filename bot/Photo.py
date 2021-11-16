import json
from io import BytesIO

from AiohttpClient import AIOHTTPClient


class PhotoBytesIO:
    def __init__(self, api, image: BytesIO, client=None):
        self._api = api
        self.image = image
        self._client = client or AIOHTTPClient()

        if not hasattr(self.image, "name"):
            try:
                setattr(self.image, "name", "photo.png")
            except AttributeError:
                raise RuntimeError("'bytes' object has no attribute 'name', put your bytes in BytesIO")

    async def upload_photo_attachment(self, peer_id=2000000001):
        upload_url = (await self._api.photos.get_messages_upload_server(peer_id=peer_id)).response.upload_url

        upload_data = json.loads(
            await self._client.request_text(method="POST", url=upload_url, data={"file1": self.image})
        )

        photo = (
            await self._api.photos.save_messages_photo(
                photo=upload_data["photo"],
                server=upload_data["server"],
                hash=upload_data["hash"],
            )
        ).response[-1]

        return (
            f"photo{photo.owner_id}_{photo.id}"
            if not photo.access_key
            else f"photo{photo.owner_id}_{photo.id}_{photo.access_key}"
        )
