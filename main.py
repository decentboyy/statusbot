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
             api_id=int(os.getenv("28330381")),
             api_hash=os.getenv("6647d9d827e9e1fdb810c1b27cef423b"),
             session_string=os.getenv("BQGwSY0AqK0LySN4sa_bNvk_UexxgRsibItUMRYKznLn9qMCN6S1Ih9gRW3fprrxN_XctoW8rTxI2Es5uQh_F9-Uk5ow9yKvLfX-ylU1hkM598mTRqIr-tMpQqd0n9AfUkjE8pSCtcxeFZaYIsMaPqDUdSIPJFtJie0RnsQJYcnOOkXT63up0WlPNprlLRecSViy2cAJS8GqX2z89u825Lad3HI-cTO7_jryGfBfTCNmVUiFivysys5dFglXaEzXCvqcbQWnYnCvoSTm2ru3MwQYLWJDr_1lDt2a3JeDA207KBtep0crQ9Q09HJrF7zv-_xnMdoyhyuE_9QBSVkHdvbcKlyTqAAAAAFAylHOAA"))

bot = Client(name="st_bot",
             api_id=int(os.getenv("28330381")),
             api_hash=os.getenv("6647d9d827e9e1fdb810c1b27cef423b"),
             bot_token=os.getenv("1719065252:AAFvVycbnICjZXuH5SyV9wfJ3VGDdFvRPhg"))

BOT_LIST = [x.strip() for x in os.getenv("OctaveOneBot OctaveTwoBot eunseo_robot Miss_Anjali_Robot Octave_AFK_BOT OctaveRadioBot OctaveTagAllBot Octavemanagerbot grphlpsecurityrobot PETRICIA_ROBOT OctaveAntiChannelBot").split(' ')]
CHANNEL_OR_GROUP_ID = int(os.getenv("-1001678759604"))
MESSAGE_ID = int(os.getenv("13"))
TIME_ZONE = os.getenv("Asia/Kolkata")
OWNER_ID = int(os.getenv("5381968334"))


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
