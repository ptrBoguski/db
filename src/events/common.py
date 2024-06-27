from bot import bot
from commands.notification import set_notification_channel
from utils.data_fetch import fetch_and_analyze_rsi


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    fetch_and_analyze_rsi.start()
    await bot.sync_commands()


@bot.event
async def on_guild_join(guild):
    print(f"Joined new guild: {guild.name}")
    # Send a welcome message to the system channel if available
    if guild.system_channel:
        await guild.system_channel.send(f"Thank you for inviting me to {guild.name}!")
