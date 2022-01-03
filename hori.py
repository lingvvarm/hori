import discord 
from discord.ext import commands
import TenGiphPy

client = discord.Client()
client = commands.Bot(command_prefix='h.')
t = TenGiphPy.Tenor(token='token here')

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
	if 'доброеутрохори' in message.content.lower().replace(' ', '').replace(',', ''):
		author = str(message.author)
		embed = discord.Embed(
			title = 'Доброе утро, {0}-сэмпай'.format(author[:len(author)-5]),
			color = 0xe91e63)
		embed.set_image(url=t.random('anime hug'))
		await message.channel.send(embed=embed)
	await client.process_commands(message)

#Анти-капс
	if message.content.isupper() and 'кто я' not in message.content.lower():
		author = str(message.author)[:len(str(message.author))-5]
		if author != 'Hori':		
			embed = discord.Embed(
				description = 'Не капси, пожалуйста' + message.author.mention,
				color = 0xe74c3c)
			embed.set_image(url=t.random('anime girl sad'))
		await message.channel.send(embed=embed)	



@client.command()
async def hug(ctx, *, giftag):
    """This command will return a tenor gif if you type "!tenor cat" as example."""
    getgifurl = t.random(str(giftag))
    await ctx.send()




client.run('discord token here')