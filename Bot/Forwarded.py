class ForwardedMessages:
    def __init__(self, obj):
        self.obj = obj

    def find_quote(self):
        if not self.obj.message['text'] and self.obj.message.fwd_messages:
            authors = list(set([msg['from_id'] for msg in self.obj.message.fwd_messages]))
            if len(authors) == 1:
                quote = []
                for msg in self.obj.message.fwd_messages:
                    if msg['text']:
                        quote.append(msg["text"])
                return {authors[0]: ', '.join(quote)}
            else:
                quote = {}
                for msg in self.obj.message.fwd_messages:
                    if msg['text']:
                        quote.update({msg['from_id']: msg['text']})
                return quote
