import textwrap as tw
from os import remove

import requests
from PIL import ImageOps, Image, ImageFilter, ImageDraw, ImageFont

from BotApi import Vk


def choose_font_size(symbols):
    if symbols <= 50:
        return 80, 15
    elif symbols <= 80:
        return 65, 20
    elif symbols <= 130:
        return 50, 27
    elif symbols <= 225:
        return 40, 33
    return 33, 40


class SingleQuote:
    def __init__(self, quote, reg=False):
        self.quote = quote
        self.id = quote[0]
        if self.id > 0:
            self.quote_font_size, self.wrap_fill = choose_font_size(len(quote[1]))
            self.quote_text = ''
            for i in quote[1].replace('ё', 'е').split('\n'):
                self.quote_text += self.prepare_text(i, reg) + '\n'
            self.quote_text.rstrip('\n')
            self.Vk = Vk()

    def prepare_text(self, text, reg):
        if not reg:
            text = text.capitalize()
        prepared_quote = tw.fill(text, width=self.wrap_fill)
        return prepared_quote

    def get_author_name(self, author_id):
        return ' '.join(list(self.Vk.UserNameGet(author_id)))

    def get_author_picture(self, author_id):
        p = requests.get(self.Vk.UserPhotoGet(author_id))
        out = open(f"work/{author_id}.jpg", "wb")
        out.write(p.content)
        out.close()
        author_photo = ImageOps.grayscale(Image.open(f'work/{author_id}.jpg')).resize((800, 800), Image.ANTIALIAS).crop((0, 80, 800, 720)).filter(ImageFilter.BLUR)
        remove(f'work/{author_id}.jpg')
        return author_photo

    def assembly(self):
        if self.id > 0:
            author_photo = self.get_author_picture(self.id)
            name = self.get_author_name(self.id)
            template = Image.open('../sources/templates/template.png').resize((800, 640), Image.ANTIALIAS)
            ready_to_text = Image.alpha_composite(author_photo.convert('RGBA'), template.convert('RGBA'))

            draw = ImageDraw.Draw(ready_to_text)
            name_font = ImageFont.truetype('../sources/fonts/signature.ttf', 30)
            name_width = draw.textsize(name, font=name_font)[0]
            draw.text((800 - (30 + name_width), 580), name, font=name_font)

            quote_font = ImageFont.truetype('../sources/fonts/main.ttf', self.quote_font_size)
            top = 0
            lines = self.quote_text.rstrip('\n').split('\n')
            all_quote_height = len(lines) * self.quote_font_size

            if all_quote_height <= 600 and len(lines) <= 11:
                start_top = 640 - all_quote_height + 10
                for line in lines:
                    quote_size = draw.textsize(line, font=quote_font)
                    draw.text(((800 - quote_size[0]) // 2, start_top // 2 + top), line, font=quote_font)
                    top += self.quote_font_size

                ready_to_text.save(f'work/temp{self.id}.png')
                return f'work/temp{self.id}.png'
        return None

