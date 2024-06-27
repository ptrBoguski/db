import discord
from discord.ext import commands
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


if __name__ == "__main__":
    from utils.data_fetch import initialize_database
    from events.common import *

    print("chuj")

    initialize_database()
    print(BOT_TOKEN)
    bot.run(BOT_TOKEN)
