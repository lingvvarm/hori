import discord 
from discord.ext import commands
from dislash import InteractionClient
import TenGiphPy
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io

headers = {"User-Agent": "hori_bot"}

client = discord.Client()
client = commands.Bot(command_prefix='h.')
inter_client = InteractionClient(client)
t = TenGiphPy.Tenor(token='NK5M66O2GA67')

def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = text[:mid]
        w, h = draw.textsize(t, font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = text[:lo]
    w, h = draw.textsize(t, font=font)
    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)


def fit_text(img, text, color, font):
    width = img.size[0] - 2
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text, width, font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = (img.size[1] - height) // 1.03
    for t, w, h in pieces:
        x = (img.size[0] - w) // 2
        draw.text((x, y), t, font=font, stroke_width=2, stroke_fill='black')
        y += h


# Уведомление об успешном логе
@client.event
async def on_ready():
	print('Logged on as {0}!'.format(client.user))


#Функция ответа на сообщение
@client.event
#кто я; ты дэб
async def on_message(message):
	if 'кто я' in message.content.lower():
		if message.content.isupper():
			await message.channel.send('ТЫ ДЭБ')
		else:
			await message.channel.send('ты дэб')


#доброе утро
	if 'доброеутро' in message.content.lower().replace(' ', '').replace(',', ''):
		author = str(message.author)
		embed = discord.Embed(
			title = 'Доброе утро, {0}-сэмпай'.format(author[:len(author)-5]),
			color = 0xe91e63)
		embed.set_image(url=t.random('anime hug'))
		await message.channel.send(embed=embed)
	await client.process_commands(message)

#Анти-капс
	# if message.content.isupper() and 'кто я' not in message.content.lower():
	# 	author = str(message.author)[:len(str(message.author))-5]
	# 	if author != 'Hori':		
	# 		embed = discord.Embed(
	# 			description = 'Не капси, пожалуйста' + message.author.mention,
	# 			color = 0xe74c3c)
	# 		embed.set_image(url=t.random('anime girl sad'))
	# 	await message.channel.send(embed=embed)

#Анти дима
	if (message.author.id == 631219894100295700 or message.author.id == 349886496788185108) and message.channel.id == 788494634216980510:
		await message.channel.send('Дім стулись нахуй)')
		await message.delete()
		


@client.command(brief="Поиск аниме на Шикимори по названию.", description="Поиск аниме на Шикимори по названию аниме. На вход принимается название аниме.")
async def anime(ctx, *, anime_name):
	r = requests.get(f"https://shikimori.one/api/animes?kind=tv&search={anime_name}", headers=headers)
	
	if r.status_code != 200:
		print(f"Error: {r.status_code}")
	else:
		data = r.json()[0]
		name = data['russian']
		link = f"https://shikimori.one{data['url']}"
		status = data['status']
		preview = f"https://shikimori.one{data['image']['original']}"

		await ctx.send(name)
		await ctx.send(link)
	

@client.command(brief="Поиск персонажа на Шикимори по имени.", description="Использование: h.char <имя персонажа> Поиск персонажа на Шикимори по имени персонажа.")
async def char(ctx, *, char_name):
	r = requests.get(f"https://shikimori.one/api/characters/search?search={char_name}", headers=headers)
	if r.status_code != 200:
		print(f"Error: {r.status_code}")
	else:
		data = r.json()[0]
		name = data['russian']
		image = f"https://shikimori.one{data['image']['original']}"
		url = f"https://shikimori.one{data['url']}"
		embed = discord.Embed(
			title = name,
			color = 0xe91e63,
			url = url)
		embed.set_image(url=image)
		
		await ctx.send(embed=embed)


@client.command(brief="Рандомные аниме картинки.", description="Использование: h.waifu <категория> <sfw или nsfw> Категории: waifu, neko, shinobu, megumin, bully, cuddle, cry, hug, awoo, kiss, lick, pat, smug, bonk, yeet, blush, smile, wave, highfive, handhold, nom, bite, glomp, slap, kill, kick, happy, wink, poke, dance, cringe\n Для nsfw после название категории наберите nsfw.")
async def waifu(ctx, category, type='sfw'):
	r = requests.get(f"https://api.waifu.pics/{type}/{category}")
	if r.status_code == 200:
		data = r.json()
		image = data['url']
		await ctx.send(image) 
		await ctx.message.delete() 

@client.command(brief="Мемы с Шелби.", description="Генерит мемы с Шелби. Использование: h.shelby <номер картинки от 1 до 6> <текст>")
async def shelby(ctx, sample=3, *,text):
    if len(text) == 0:
        await ctx.send("Немає тексту")
        return 1
    # if len(text) > 25:
    #     await ctx.send("Занадто довгий текст")
    #     return 1
    img = Image.open(f'samples/{sample}resize.jpg')
    w, h = img.size
    my_image = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("impact.ttf", 48)
    text_w, text_h = my_image.textsize(text, font)
    #my_image.text(((w - text_w) // 2, h - text_h - 15), text, (255,255,255), font=font, stroke_width=2, stroke_fill='black')
    fit_text(img, text, (255, 255, 255), font)

    with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='meme.png'))
    await ctx.message.delete()




client.run('ODU4NzU3NDk3OTAxMTU0MzQ0.G_1fRt.UmeYkRvoDqFf26vmyy6PecXHJ8OZKUo8Cxy7-4')
