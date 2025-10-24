import os
import discord
from discord.ext import tasks
import requests
import asyncio

from myserver import server_on

# ====== CONFIG ======
TOKEN = "YOUR_BOT_TOKEN"            # 🔹 ใส่โทเคนบอทที่ได้จาก Discord
CHANNEL_ID = 123456789012345678     # 🔹 ใส่ Channel ID ที่จะส่งข้อความ
TARGET_PRICE = 5.0                  # 🔹 ราคาที่ต้องการให้แจ้งเตือน (USD)
CHECK_INTERVAL = 60                 # 🔹 ตรวจสอบทุก 60 วินาที

COIN_ID = "worldcoin"

# ====== Discord Client ======
intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_wld_price():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={COIN_ID}&vs_currencies=usd"
    r = requests.get(url)
    data = r.json()
    return data[COIN_ID]["usd"]

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    check_price.start()  # เริ่ม loop ตรวจสอบราคา

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_price():
    try:
        price = get_wld_price()
        print(f"ราคา WLD ตอนนี้: {price} USD")

        if price >= TARGET_PRICE:
            channel = client.get_channel(CHANNEL_ID)
            if channel:
                msg = f"🚨 แจ้งเตือน! ราคาเหรียญ **WLD** ถึงเป้าหมายแล้ว: {price} USD 🎯"
                await channel.send(msg)
                check_price.stop()  # หยุด loop หลังส่งแจ้งเตือน
    except Exception as e:
        print("❌ Error:", e)

server_on()

client.run(os.getenv('TOKEN'))
