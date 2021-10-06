import requests
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from Api import get_user_name, get_user_photo, upload_message_photo, send_message, api, GROUP_ID, CONSOLE
from Exceptions import PredException
from Processing import extract_forwarded, filter_author, recursive_extract_forwarded
from QuotesGen import SingleQuote


def parse_quotes_options(message_text):
    rec = None

    if "/" in message_text:
        if any([i in message_text for i in ["r", "р", "rec", "recursive", "рек", "рекурсия"]]):
            rec = True
        else:
            rec = False

    return rec


def new_message(message):
    text = message["text"]
    peer_id = message["peer_id"]
    forwarded = message["fwd_messages"]
    reply = message.get("reply_message")

    if any([i in text for i in ["help", "хелп", "помощь"]]):
        send_message(peer_id, "Хелп всея Предикатов\n\n"
                              "- Реплай или пересланное сообщение - генерация цитаты (в беседах надо упоминать!)\n"
                              "- /r в сообщении - рекурсивный обход пересланных сообщений (включено по дефолту)\n\n"
                              "Скоро заебашу еще приклюх. Самые кеки присылайте в предложку @prediquotes")
    if reply:
        quote_assembly([reply], peer_id)
    else:
        rec = parse_quotes_options(text)
        if not (rec is None):
            quote_assembly(forwarded, peer_id, rec)
        else:
            try:
                quote_assembly(forwarded, peer_id)
            except PredException:
                quote_assembly(forwarded, peer_id, True)
            except Exception as e:
                PredException("Чета не то, не получилось найти текст в сообщениях ни прямо, ни рекурсивно.\n"
                              "Тут либо ты долюоеб, либо я")
                send_message(CONSOLE, str(e))


def quote_assembly(forwarded, peer_id, rec=False):
    if not rec:
        quote_obj = filter_author(extract_forwarded(forwarded))
    else:
        quote_obj = filter_author(recursive_extract_forwarded(forwarded))

    if "".join(quote_obj[1]):
        result_quote = SingleQuote("\n".join(quote_obj[1]),
                                   get_user_photo(quote_obj[0]),
                                   get_user_name(quote_obj[0])).assembly()

        send_message(peer_id, attachment=upload_message_photo(result_quote))
    else:
        raise PredException('Че за хуйня? Где текст в сообщениях?\nЕбани "@prediquotes хелп" если чо')


def main_bot():
    print('LongPooling started!')
    while True:
        try:
            for event in VkBotLongPoll(api, group_id=GROUP_ID).listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    try:
                        new_message(event.object["message"])
                    except PredException as e:
                        send_message(event.object["message"]["peer_id"], message=e)
                    except Exception:
                        send_message(event.object["message"]["peer_id"], message='Чет ты хуйню делаешь, тут так не принято\nЧитай "@prediquotes help" и делай как там')
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    main_bot()
