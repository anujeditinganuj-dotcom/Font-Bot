import os
from datetime import datetime
from pytz import timezone
from pyrogram import Client, filters, enums
from pyrogram.types import Message, BotCommand
from aiohttp import web
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN, LOG_CHANNEL

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route(request):
    return web.Response(text="<h3 align='center'><b>I am Alive</b></h3>", content_type='text/html')

async def web_server():
    app = web.Application(client_max_size=30_000_000)
    app.add_routes(routes)
    return app

class Bot(Client):
    def __init__(self):
        super().__init__(
            "techifybots",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechifyBots"),
            workers=200,
            sleep_threshold=15
        )

    async def start(self):
        app = web.AppRunner(await web_server())
        await app.setup()
        try:
            await web.TCPSite(app, "0.0.0.0", int(os.getenv("PORT", 8080))).start()
            print("Web server started.")
        except Exception as e:
            print(f"Web server error: {e}")

        await super().start(**kwargs)
        me = await self.get_me()
        print(f"Bot Started as {me.first_name}")

        if LOG_CHANNEL:
            try:
                now = datetime.now(timezone("Asia/Kolkata"))
                msg = (
                    f"<blockquote>🚀 <b>{me.mention} Started!</b>\n\n"
                    f"📅 <b>Date :</b> <code>{now.strftime('%d %B, %Y')}</code>\n"
                    f"⏰ <b>Time :</b> <code>{now.strftime('%I:%M:%S %p')}</code>\n"
                    f"🌐 <b>Timezone :</b> <code>Asia/Kolkata</code>\n\n"
                    f"👑 <b>Developed by @anujedits76</b></blockquote>"
                )
                await self.send_message(LOG_CHANNEL, msg, parse_mode=enums.ParseMode.HTML)
            except Exception as e:
                print(f"Error sending to LOG_CHANNEL: {e}")

        await self.set_bot_commands_list()

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped.")

    async def set_bot_commands_list(self):
        commands = [
            BotCommand("start",     "🚀 ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
            BotCommand("help",      "📚 ʜᴏᴡ ᴛᴏ ᴜꜱᴇ"),
            BotCommand("about",     "ℹ️ ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ"),
            BotCommand("broadcast", "📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ (ᴀᴅᴍɪɴ)"),
            BotCommand("stats",     "👥 ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ (ᴀᴅᴍɪɴ)"),
            BotCommand("ban",       "🔨 ʙᴀɴ ᴀ ᴜꜱᴇʀ (ᴀᴅᴍɪɴ)"),
            BotCommand("unban",     "✅ ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ (ᴀᴅᴍɪɴ)"),
            BotCommand("banned",    "📋 ʙᴀɴɴᴇᴅ ʟɪꜱᴛ (ᴀᴅᴍɪɴ)"),
            BotCommand("cmd",       "🔄 ᴜᴘᴅᴀᴛᴇ ᴄᴏᴍᴍᴀɴᴅꜱ (ᴀᴅᴍɪɴ)"),
        ]
        await self.set_bot_commands(commands)


BotInstance = Bot()


@BotInstance.on_message(filters.command("cmd") & filters.user(ADMIN))
async def update_commands(bot: Client, message: Message):
    try:
        await BotInstance.set_bot_commands_list()
        await message.reply_text(
            "<b>✅ ᴄᴏᴍᴍᴀɴᴅꜱ ᴍᴇɴᴜ ᴜᴘᴅᴀᴛᴇᴅ!</b>",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(
            f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>",
            parse_mode=enums.ParseMode.HTML
        )


BotInstance.run()
