from bot import bot
import sqlite3
from utils import data_fetch


@bot.slash_command(
    name="set_channel", description="Set this channel to receive notifications."
)
async def set_notification_channel(ctx):
    guild_id = ctx.guild.id
    channel_id = ctx.channel.id

    with sqlite3.connect("bot_data.db") as conn:
        c = conn.cursor()
        c.execute(
            "REPLACE INTO notification_channels (guild_id, channel_id) VALUES (?, ?)",
            (guild_id, channel_id),
        )
        conn.commit()

    await ctx.respond(f"Notifications will now be sent to {ctx.channel.mention}")


@bot.slash_command(name="get_recent_rsi", description="returns current rsi value")
async def get_recent_rsi(ctx):
    guild_id = ctx.guild.id
    channel_id = ctx.channel.id

    await ctx.respond(
        f"latest RSI value is: {data_fetch.fetch_and_analyze_rsi.previous_rsi}"
    )
