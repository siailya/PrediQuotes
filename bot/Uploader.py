import json

from aiohttp import ClientSession


class PhotoUploader:
    @staticmethod
    async def get_server(api, peer_id: int) -> str:
        server_data = await api.photos.get_messages_upload_server(peer_id=peer_id)
        return server_data.response.upload_url

    @staticmethod
    async def request_text(method: str, url: str, data=None) -> str:
        data = data or {}

        async with ClientSession().request(method, url, data=data) as resp:
            return await resp.text()

    async def upload(
            self,
            api,
            upload_url: str,
            file_data,
            file_name=None,
            file_extension=None,
    ):
        file_name = file_name or "Photo"
        file_extension = file_extension or "jpg"
        if not hasattr(file_data, "name"):
            try:
                setattr(file_data, "name", f"{file_name}.{file_extension}")
            except AttributeError:
                raise RuntimeError(
                    "'bytes' object has no attribute 'name', put your bytes in BytesIO"
                )

        upload_data = json.loads(
            await self.request_text(
                method="POST", url=upload_url, data={"file1": file_data}
            )
        )

        photo_sizes = (
            await api.photos.save_messages_photo(
                photo=upload_data["photo"],
                server=upload_data["server"],
                hash=upload_data["hash"],
            )
        ).response
        return photo_sizes
