from vkwave.api import APIOptionsRequestContext

from AnswerStrategy import AnswerStrategyFactory
from utils import get_random_id


class Message:
    def __init__(self, api: APIOptionsRequestContext, loop, msg_object):
        self._api = api
        self._loop = loop
        self._object = msg_object
        self.from_id = self._object["from_id"]
        self.peer_id = self._object["peer_id"]
        self.text = self._object["text"]
        self.is_from_user = self.from_id >= 1
        self.result_args = []

    async def answer(self):
        await AnswerStrategyFactory(self._object).get_strategy()(self, loop=self._loop, api=self._api).submit()

    def _parse_message_args(self):
        dispatch_args = {
            "quo": ["q", "quote", "ц", "цитата"],
            "rec": ["rec", "рек", "рекурсия", "recursive"]
        }
        self.result_args = []

        for arg in dispatch_args.keys():
            if any([i in self.text for i in dispatch_args[arg]]):
                self.result_args.append(arg)

        return self.result_args

    def get_forwarded(self):
        return self._object.get("fwd_messages", [])

    def get_reply(self):
        return self._object.get("reply_message", None)

    def get_raw(self):
        return self._object

    def get_args(self):
        return self._parse_message_args()

    def get_text(self):
        return self.text
