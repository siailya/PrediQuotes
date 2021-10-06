

def leave_excess(t):
    t = t.split("/")[0].strip()
    return t.replace("[club172694092|@prediquote]", "").strip()


def recursive_extract_forwarded(forwarded):
    res = []

    for f in forwarded:
        if f.get("fwd_messages"):
            for i in [(leave_excess(f["text"]), f["from_id"])] + recursive_extract_forwarded(f.get("fwd_messages")):
                res.append(i)
        else:
            res.append((leave_excess(f["text"]), f["from_id"]))

    return list(filter(lambda x: x[0].strip() != "", res))


def extract_forwarded(forwarded):
    res = []

    for f in forwarded:
        res.append((leave_excess(f["text"]), f["from_id"]))

    return res


def filter_author(messages, most=True, author=None):
    mu = {}

    for i in messages:
        mu.update({i[1]: mu.get(i[1], 0) + 1})

    author = list({k: v for k, v in sorted(mu.items(), key=lambda item: item[1])}.keys())[-1]

    return author, list(map(lambda x: x[0], filter(lambda x: x[1] == author, messages)))

