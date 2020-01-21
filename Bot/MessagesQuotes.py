class MessagesQuotes:
    def __init__(self, obj):
        self.obj = obj

    def find_quote(self):
        authors = list(set([msg['from_id'] for msg in self.obj.message.fwd_messages]))
        if len(authors) == 1:
            quote = []
            for msg in self.obj.message.fwd_messages:
                if msg['text']:
                    quote.append(msg["text"])
            if quote:
                return [authors[0], '\n'.join(quote)]
            return None
        else:
            quote = []
            for msg in self.obj.message.fwd_messages:
                if msg['text']:
                    if quote:
                        if quote[-1][0] == msg['from_id']:
                            quote[-1][1] += f'\n{msg["text"]}'
                        else:
                            quote.append([msg['from_id'], msg['text']])
                    else:
                        quote.append([msg['from_id'], msg['text']])
            return quote if quote else None


def single_quote(quote):
    if len(quote) == 2 and type(quote[0]) is int:
        return True
    return False