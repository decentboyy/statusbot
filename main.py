import os
import asyncio
import datetime
import pytz

from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import FloodWait

load_dotenv()

app = Client(name="st_userbot",
             api_id=int(os.getenv("API_ID")),
             api_hash=os.getenv("API_HASH"),
             session_string=os.getenv("SESSION_STRING"))

bot = Client(name="st_bot",
             api_id=int(os.getenv("API_ID")),
             api_hash=os.getenv("API_HASH"),
             bot_token=os.getenv("BOT_TOKEN"))

BOT_LIST = [x.strip() for x in os.getenv("BOT_LIST").split(' ')]
CHANNEL_OR_GROUP_ID = int(os.getenv("CHANNEL_OR_GROUP_ID"))
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
TIME_ZONE = os.getenv("TIME_ZONE")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot.start()


import psutil
import time
from _ import start_time, Client # replace _ where you declare the start_time, Client
from pyrogram import filters 
from pyrogram.types import Message

# TeamUltroid/Ultroid
def time_formatter(milliseconds):
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (((str(weeks) + "w:") if weeks else "") +
           ((str(days) + "d:") if days else "") +
           ((str(hours) + "h:") if hours else "") +
           ((str(minutes) + "m:") if minutes else "") +
           ((str(seconds) + "s") if seconds else ""))
    if not tmp:
        return "0s"
    if tmp.endswith(":"):
        return tmp[:-1]
    return tmp


@Client.on_message(filters.command('statusbot') & filters.private)
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    TEXT = f"UPTIME: {uptime} | CPU: {cpu}%"
    await message.reply(TEXT)


bot.run(main())
