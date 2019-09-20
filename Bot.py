import asyncio
import discord
import requests
from discord.ext.commands import Bot
from discord import Game
from bs4 import BeautifulSoup
from urllib.parse import unquote

client = Bot(command_prefix = "/")

async def Google(q):
	searchpage = requests.get("https://www.google.com/search?q={}".format(q))
	bsoup = BeautifulSoup(searchpage.content, 'html.parser')
	message = " "
	results = bsoup.findAll("div", attrs={"class":"g"})
	for result in results:
		h3 = result.find("h3", attrs={"class":"r"}, recursive=True)
		if h3 != None:
			a = h3.find("a")
			txt = h3.text
			link = a.get("href")
			link = link.replace("/url?q=", "")
			link = link.replace("/search?", "https://www.google.com/search?")
			link = link[:link.rfind("&sa=U")]
			link = unquote(link)
			message += "{}\n{}\n\n".format(txt,link)
			if len(message) > 1600:
				break
	return message

@client.command(pass_context=True)
async def google(context, args="Google"):
    if len(args) > 1:
        try:
            searchQuery = "".join(args[0:])
            messageString = await Google(searchQuery)
            em = discord.embed(title="\"{}\"Google search results for".format(searchQuery), description=messageString, colour=0x8FACEf)
            await client.send_message(context.message.channel, embed=em)
        except:
            await client.send_message(context.message.channel, "Can't get search results from Google")

@client.event
async def on_ready():
    await client.change_presence (game= Game(name="google <search word>"))
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run("NjE0MDcyNjc4NDM3MDkzMzk2.XYSAFw.LELfyj_Gz9tPLPWIaXTZr6its8s")
