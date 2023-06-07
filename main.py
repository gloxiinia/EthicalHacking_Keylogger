import discord
from discord.ext import commands

#token constant for the bot
TOKEN = "hehe token owo"

#getting the client from discord.py (aka the bot)
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# event listener from when the bot goes from offline to online
@bot.event
async def on_ready():
	#counter for amount of guilds/servers the bot is in
	guild_count = 0
	
    #for loop counting the bot
	for guild in bot.guilds:
		print(f"- {guild.id} (name: {guild.name})")  #print server id and name
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
	print("Keylogger is in " + str(guild_count) + " guilds.")

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.command()
async def hello(ctx):
    await ctx.send('Hello, world!')

bot.run(TOKEN)