import textwrap as tw
from io import BytesIO

import requests
from PIL import ImageOps, Image, ImageFilter, ImageDraw, ImageFont

from Exceptions import PredException


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


def get_photo_from_url(photo_url):
    response = requests.get(photo_url)
    img = ImageOps.grayscale(Image.open(BytesIO(response.content))).resize((800, 800), Image.ANTIALIAS).crop(
        (0, 80, 800, 720)).filter(ImageFilter.BLUR)
    return img


class SingleQuote:
    def __init__(self, quote, photo_url, namelist, reg=False):
        self.name = namelist[0]
        self.surname = namelist[1]
        self.fullname = (namelist[0] + " " + namelist[1]).strip()
        self.photo_url = photo_url
        self.img = None
        self.quote_font_size, self.wrap_fill = choose_font_size(len(quote))
        self.quote_text = ''

        for i in quote.replace('ё', 'е').split('\n'):
            self.quote_text += self.prepare_text(i, reg) + '\n'
        self.quote_text.rstrip('\n')

    def prepare_text(self, text, reg):
        if not reg:
            text = text.capitalize()
        prepared_quote = tw.fill(text, width=self.wrap_fill)
        return prepared_quote

    def assembly(self):
        author_photo = get_photo_from_url(self.photo_url)

        template = Image.open('sources/templates/template.png').resize((800, 640), Image.ANTIALIAS)
        ready_to_text = Image.alpha_composite(author_photo.convert('RGBA'), template.convert('RGBA'))

        draw = ImageDraw.Draw(ready_to_text)
        name_font = ImageFont.truetype('./sources/fonts/signature.ttf', 30)
        name_width = draw.textsize(self.fullname, font=name_font)[0]
        draw.text((800 - (30 + name_width), 580), self.fullname, font=name_font)

        quote_font = ImageFont.truetype('./sources/fonts/main.ttf', self.quote_font_size)
        top = 0
        lines = self.quote_text.rstrip('\n').split('\n')
        all_quote_height = len(lines) * self.quote_font_size

        if all_quote_height <= 600 and len(lines) <= 11:
            start_top = 640 - all_quote_height + 10
            for line in lines:
                quote_size = draw.textsize(line, font=quote_font)
                draw.text(((800 - quote_size[0]) // 2, start_top // 2 + top), line, font=quote_font)
                top += self.quote_font_size

            image_handle = BytesIO()
            ready_to_text.save(image_handle, "PNG")
            image_handle.seek(0)

            return image_handle
        raise PredException("Слишком большая цитата! Текст будет пизда мелкий...")
