import time
import requests
import pandas as pd
import ta
from discord.ext import tasks
from bot import bot
from config import SYMBOL, INTERVAL
from datetime import datetime, timedelta
import sqlite3


def initialize_database():
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS notification_channels (
            guild_id INTEGER PRIMARY KEY,
            channel_id INTEGER
        )
    """
    )
    conn.commit()
    conn.close()


def get_notification_channels():
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("SELECT channel_id FROM notification_channels")
    channels = [row[0] for row in c.fetchall()]
    conn.close()
    return channels


@tasks.loop(seconds=6)
async def fetch_and_analyze_rsi():
    if not hasattr(fetch_and_analyze_rsi, "previous_rsi"):
        fetch_and_analyze_rsi.previous_rsi = None

    url = "https://api.bybit.com/v5/market/kline"
    symbol = SYMBOL
    interval = INTERVAL
    limit = 336
    end_time = int(time.time())
    start_time = end_time - (14 * 24 * 60 * 60)

    params = {
        "category": "spot",
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "start": start_time * 1000,
        "end": end_time * 1000,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["retCode"] == 0 and data["result"]["list"]:
        kline_data = data["result"]["list"]
        df = pd.DataFrame(
            kline_data,
            columns=["start", "open", "high", "low", "close", "volume", "end"],
        )
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
    else:
        print("No data returned or error in response.")
        if "retMsg" in data:
            print(f"Error message: {data['retMsg']}")

    rsi = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    current_rsi = rsi.iloc[-1]
    print(current_rsi)

    channels = get_notification_channels()
    for channel_id in channels:
        channel = bot.get_channel(channel_id)
        if (
            fetch_and_analyze_rsi.previous_rsi == None
            or fetch_and_analyze_rsi.previous_rsi >= 30
        ) and current_rsi < 30:
            await channel.send(
                f"RSI Alert: {SYMBOL} RSI has dropped below 30! Current RSI: {current_rsi:.2f}"
            )
        elif (
            fetch_and_analyze_rsi.previous_rsi == None
            or fetch_and_analyze_rsi.previous_rsi <= 70
        ) and current_rsi > 70:
            await channel.send(
                f"RSI Alert: {SYMBOL} RSI has exceeded 70! Current RSI: {current_rsi:.2f}"
            )

    fetch_and_analyze_rsi.previous_rsi = current_rsi
