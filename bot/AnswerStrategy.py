import re
from abc import abstractmethod, ABC

from vkwave.api import APIOptionsRequestContext

from ClientsFactory import get_aiohttp_client
from Photo import PhotoBytesIO
from SingleQuote import create_quote_async
from User import User
from utils import get_random_id


class AnswerStrategyFactory:
    def __init__(self, msg_object):
        self._object = msg_object
        self.has_reply = self._get_reply_msg()
        self.has_forwarded = self._get_forwarded_msgs()

    def _get_reply_msg(self):
        return self._object.get("reply_message", None)

    def _get_forwarded_msgs(self):
        return self._object.get("fwd_messages", None)

    def get_strategy(self):
        if self.has_reply:
            return AnswerToReply
        elif self.has_forwarded:
            return AnswerToForwarded

        return BaseAnswerStrategy


class AnswerStrategy(ABC):
    def __init__(self, msg, loop, api: APIOptionsRequestContext):
        self._api = api
        self._loop = loop
        self._msg = msg
        self._object = msg.get_raw()
        self.args = msg.get_args()
        self.peer_id = self._object["peer_id"]

    @abstractmethod
    def submit(self):
        ...

    async def send_answer(self, message="", attachment=None):
        await self._api.messages.send(peer_id=self.peer_id, random_id=get_random_id(),
                                      message=message, attachment=attachment)


class BaseAnswerStrategy(AnswerStrategy):
    def __init__(self, msg, loop, api: APIOptionsRequestContext):
        super().__init__(msg, loop, api)

    async def submit(self):
        await self.send_answer("Чтобы получить цитатку, ответь на чьё-нибудь сообщение "
                               "(или перешли его) и отметь сообщество - @prediquote")


class AnswerToReply(AnswerStrategy):
    def __init__(self, msg, loop, api: APIOptionsRequestContext):
        super().__init__(msg, loop, api)
        self.reply = msg.get_reply()

    async def submit(self):
        reply_text = self.reply["text"]

        if reply_text:
            quoted_user = User(self._api, self.reply["from_id"])
            photo_url = await quoted_user.get_photo_url()
            user_name = await quoted_user.get_name()

            quoted = await create_quote_async(
                loop=self._loop,
                text=reply_text,
                author_name=user_name["full_name"],
                author_photo=photo_url
            )

            attachment = await PhotoBytesIO(self._api, quoted, client=get_aiohttp_client()) \
                .upload_photo_attachment(self.peer_id)

            await self.send_answer("Цитатка!", attachment=attachment)

        else:
            await self.send_answer('В пересланном сообщении должен быть текст!\n\n'
                                   'Для полного хелпа введите "@prediquote help"')


class AnswerToForwarded(AnswerStrategy):
    def __init__(self, msg, loop, api: APIOptionsRequestContext):
        super().__init__(msg, loop, api)
        self.forwarded = msg.get_forwarded()

    async def submit(self):
        if "rec" not in self._msg.get_args():
            filtered_msgs = self.filter_author(self.direct_extract_forwarded(self.forwarded))

        else:
            filtered_msgs = self.filter_author(self.recursive_extract_forwarded(self.forwarded))

        quoted_user = User(self._api, filtered_msgs[0])
        photo_url = await quoted_user.get_photo_url()
        user_name = await quoted_user.get_name()

        quoted = await create_quote_async(
            loop=self._loop,
            text="\n".join(filtered_msgs[1]),
            author_photo=photo_url,
            author_name=user_name["full_name"]
        )

        attachment = await PhotoBytesIO(self._api, quoted, client=get_aiohttp_client()) \
            .upload_photo_attachment(self.peer_id)

        await self.send_answer("Цитатка!", attachment)

    @staticmethod
    def _leave_excess(text):
        text = re.sub(r"\[club172694092\|[*@]prediquote\][,\s]", "", text)
        return text.strip()

    def recursive_extract_forwarded(self, forwarded_msgs):
        res = []

        for f in forwarded_msgs:
            if f.get("fwd_messages"):
                for i in [(self._leave_excess(f["text"]), f["from_id"])] + \
                         self.recursive_extract_forwarded(f.get("fwd_messages")):
                    res.append(i)
            else:
                res.append((self._leave_excess(f["text"]), f["from_id"]))

        return list(filter(lambda x: x[0].strip() != "", res))

    def direct_extract_forwarded(self, forwarded):
        res = []

        for f in forwarded:
            res.append((self._leave_excess(f["text"]), f["from_id"]))

        return res

    @staticmethod
    def filter_author(messages, most=True, author=None):
        # TODO: Фильрация по переданному автору
        mu = {}

        for i in messages:
            mu.update({i[1]: mu.get(i[1], 0) + 1})

        author = list({k: v for k, v in sorted(mu.items(), key=lambda item: item[1])}.keys())[-1]

        return author, list(map(lambda x: x[0], filter(lambda x: x[1] == author, messages)))
