import os
import asyncio
import datetime
import pytz
import psutil

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


async def get_uptime():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    return str(uptime)


async def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"{cpu_usage}%"


async def main():
    print("Status Checker Bot Started")
    async with app:
        while True:
            TEXT = "This is the live bot status of all Bots 🤖"
            for bot_username in BOT_LIST:
                bot_user = await app.get_users(bot_username)
                try:
                    await app.send_message(bot_username, "/statusbot")
                    await asyncio.sleep(2)
                    messages = await app.get_chat_history(bot_username, limit=1)
                    async for message in messages:
                        if message.text == "/statusbot":
                            TEXT += f"\n\n**🤖-[{bot_user.first_name}](tg://openmessage?user_id={bot_user.id}): OFFLINE** 💀"
                            await bot.send_message(OWNER_ID, f"Alert {bot_user.first_name} is offline 💀")
                        else:
                            uptime = await get_uptime()
                            cpu_usage = await get_cpu_usage()
                            TEXT += f"\n\n**🤖-[{bot_user.first_name}](tg://openmessage?user_id={bot_user.id}): {message.text}**"
                            TEXT += f"\nUptime: {uptime}"
                            TEXT += f"\nCPU Usage: {cpu_usage}"
                except FloodWait as e:
                    await asyncio.sleep(e.x)
            time = datetime.datetime.now(pytz.timezone(TIME_ZONE))
            date = time.strftime("%d %b %Y")
            time = time.strftime("%I:%M: %p")
            TEXT += f"\n\n--Last checked on--: \n{date}\n{time} ({TIME_ZONE})\n\n**Refreshes Automatically After Every 15 Min.**"
            await bot.edit_message_text(int(CHANNEL_OR_GROUP_ID), MESSAGE_ID, TEXT)
            await asyncio.sleep(900)


bot.run(main())
