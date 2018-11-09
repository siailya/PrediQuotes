import wand
import os
import shutil
import time
from wand.image import Image
from wand.image import Image, COMPOSITE_OPERATORS
from wand.drawing import Drawing
from wand.display import display
from PIL import Image as IMG
from PIL import ImageFont as IMGF
from PIL import ImageDraw as IMGD

# Пиздец я с этой хуетой заебался, она блять не работает нормально
# Еще и с кодировкой какие-то заебы
# Бля, сложно, получается тольок поэтапно все делать, сохраняя промежуточныяй результат
# УРААА БЛЯТЬ ОНО РАБОТАЕТ
# Бля, как же хорошо, что есть интернет и можно тупа копипастить
# Ну уже реп ебет, скоро будет готово. Наверное 
# Все, заебись!

f = open('log.txt', 'w')

gd = input('Нужно делать размытие? (рекомендуется) - y/n: ')
if gd == 'y':
	g1 = int(input('Введите радиус размытия: '))
	g2 = int(input('Введите отклонение размытия (обязательно меньше радиуса!): '))
elif gd == 'n':
	g1 = 0
	g2 = 0
else:
	print('Неправильный формат ввода! Размытие не будет применено')
	
# Создание каталога для хранения временных файлов(промежуточных результатов)
try:
	os.mkdir('temp')
except:
	try:
		os.remove('temp')
	except:
		pass

# Узнаем параметры изображения		
with Image(filename='pic.jpg') as img:
	width = img.width
	height = img.height

print('Подгоняем размеры...')
# Подгоняем изображение под формат
with Image(filename='pic.jpg') as img:
	img.sample(1500, int((1500/width) * height))
	img.save(filename='temp\picres.jpg')

# Обработка изображения - ЧБ и размытие по гауссу	
fx_filter = '(saturation < 0.01 && hue < 0.02) ? u : lightness'
with Image(filename=r'temp\picres.jpg') as img:
	print('Делаем размытие по гауссу...')
	img.gaussian_blur(g1, g2)
	print('Обесцвечиваем изображение...')
	with img.fx(fx_filter) as img2:
		img2.save(filename=r'temp\fxed.jpg')

print('Накладываем маску...')
# Наложение черной маски с кавычками
img = IMG.open(r'temp\fxed.jpg')
black = IMG.open(r'init\black.png')
img.paste(black, (0, 0), black)
img.save(r'temp\result.png')
time.sleep(0.5)

print('Обрезаем изображение...')
# Обрезание изображения
with Image(filename=r'temp\result.png') as img:
	img.crop(0, 0, width=1500, height=1200)
	img.save(filename=r'temp\final.jpg')
time.sleep(0.5)
	
# -----------------------------------------------
# Обработка текста
# -----------------------------------------------

z = 0
upcount = 0
spacecount = 0
dotcount = 0

k = int(input('Введите количество строк цитаты: '))
stri = input('Введите 1 строку цитаты: ')

h = ((1200 - ((120 * k) + (40 * k - 1))) / 2) + 75
for letter in stri:
	if letter.isupper():
		upcount += 1

for letter in stri:
	if letter == ' ':
		spacecount += 1

for letter in stri:
	if letter == '.':
		dotcount += 1

lenpxl = spacecount * 30 + upcount * 79 + (len(stri) - spacecount - upcount - dotcount) * 60 + dotcount * 12

f.write(str(len(stri) - spacecount - upcount - dotcount) + ' - кол-во символов в 1 строчке ' + '\n')
f.write(str(spacecount) + str(upcount) + '- пробелы и заглавные в 1 строчке' + ' ' + '\n')
f.write(str(lenpxl) + '- длина в пикселях 1 строчки' + '\n')

p = (1500 - lenpxl) / 2
	
f.write(str(p) + ' - начало строчки ' + str(1) + ' по горизонтали')

named = 'temp\\' + 'cpout' + '1' + '.jpg'

# Наложение текста цитаты
img = IMG.open(r'temp\final.jpg')
draw = IMGD.Draw(img)
font = IMGF.truetype(r'init\main.ttf', 120)
draw.text((p, h), stri, 'white', font=font)
img.save(named)

z += 2

for i in range(2, k + 1):
	
	spacecount = 0 
	upcount = 0
	dotcount = 0
	
	stri = input('Введите следующую строку цитаты: ')
	h += 130
	
	for letter in stri:
		if letter.isupper():
			upcount += 1

	for letter in stri:
		if letter == ' ' or letter == '?':
			spacecount += 1
			
	for letter in stri:
		if letter == '.':
			dotcount += 1

	lenpxl = spacecount * 30 + upcount * 79 + (len(stri) - spacecount - upcount - dotcount) * 60 + dotcount * 12
	
	f.write(str(len(stri) - spacecount - upcount - dotcount) + ' - кол-во символов в строчке ' + str(i) + ' ' + '\n')
	f.write(str(spacecount) + str(upcount) + '- пробелы и заглавные в строчке ' + str(i) + ' ' + '\n')
	f.write(str(lenpxl) + '- длина в пикселях строчки' + str(i) + ' ' + '\n')

	p = (1500 - lenpxl) / 2
	
	f.write(str(p) + ' - начало строчки ' + str(i) + ' по горизонтали')
	
	named = 'temp\\' + 'cpout' + str(i) + '.jpg'
	opened = 'temp\\' + 'cpout' + str(i - 1) + '.jpg'
	
	# Наложение текста цитаты
	img = IMG.open(opened)
	draw = IMGD.Draw(img)
	font = IMGF.truetype(r'init\main.ttf', 120)
	draw.text((p, h), stri, 'white', font=font)
	img.save(named)

	z += 1

print('Пишем текст...')
os.rename('temp\\' + 'cpout' + str(k) + '.jpg', r'temp\finalres.jpg')

print('')
for i in range(1, k):
	os.remove('temp\\' + 'cpout' + str(i) + '.jpg')



namecp = input('Введите имя автора цитаты: ')
img = IMG.open(r'temp\finalres.jpg')
draw = IMGD.Draw(img)
font = IMGF.truetype(r'init\sig.ttf', 100)
draw.text((520, 1040), namecp, 'white', font=font)
img.save(r'Result.jpg')
print('Подписываем цитату...')
time.sleep(0.3)
print('Чистим временные папки...')
print('')
try:
	os.remove('temp')
except:
	folder = 'temp'
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)
			
f.close()

print('Готово! Результат находится в коренной папке')
close = input('Для завершения работы программы нажмите любую клавишу... ')
