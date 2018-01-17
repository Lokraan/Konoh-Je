
import asyncio
import json
import sys
import os

import discord

sys.path.append(os.path.realpath(os.path.dirname(__file__)) + "/nmt_chatbot/sentdex_lab")

from nmt_chatbot.sentdex_lab import modded_inference as inf


CONFIG_FILE = "config.json"

class Bot:
	def __init__(self, client: discord.Client):
		self._client = client

	async def greet(self, message: discord.Message):
		await self._client.send_message(
			message.channel, "Hello {0.author.mention} !".format(message)
			)

	async def speak(self, message: discord.Message):
		await self._client.send_message(
			message.channel, "{0.author.mention} {1}".format(message,
				inf.get_best_answer(
					inf.internal_inferance(message.content)
					)
				)
			)

def get_config() -> dict:
	with open(CONFIG_FILE, "r") as f:
		return json.load(f)

if __name__ == '__main__':

	client = discord.Client()

	config = get_config()

	token = config["token"]
	prefix = config["command_prefix"]

	bot = Bot(client=client) 

	@client.event
	async def on_ready():
		print("Logged in as {}".format(client.user.name))


	@client.event
	async def on_message(message: discord.Message):
		content = message.content

		if content.startswith("{}greet".format(prefix)):
			await bot.greet(message)

		elif content.startswith(prefix):
			await bot.speak(message)


	client.run(token)