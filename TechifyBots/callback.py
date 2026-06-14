from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from Script import text
from config import ADMIN
from .commands import fetch_random_image, make_button, BUTTON_STYLE_SUPPORTED
from .commands import ICON_INFO, ICON_HELP, ICON_BACK, ICON_CLOSE, ICON_CHANNEL, ICON_FEEDBACK, ICON_DEV

try:
    from pyrogram.enums import ButtonStyle
except ImportError:
    pass


def get_help_buttons():
    if BUTTON_STYLE_SUPPORTED:
        S = ButtonStyle
        return InlineKeyboardMarkup([
            [make_button(" 📢 ᴜᴘᴅᴀᴛᴇꜱ ", url="https://telegram.me/anujedits76",
                         icon_custom_emoji_id=ICON_CHANNEL, style=S.PRIMARY)],
            [make_button(" ⬅️ ʙᴀᴄᴋ ", callback_data="start",
                         icon_custom_emoji_id=ICON_BACK, style=S.PRIMARY),
             make_button(" ❌ ᴄʟᴏꜱᴇ ", callback_data="close",
                         icon_custom_emoji_id=ICON_CLOSE, style=S.DANGER)]
        ])
    else:
        return InlineKeyboardMarkup([
            [make_button(" 📢 ᴜᴘᴅᴀᴛᴇꜱ ", url="https://telegram.me/anujedits76",
                         icon_custom_emoji_id=ICON_CHANNEL)],
            [make_button(" ⬅️ ʙᴀᴄᴋ ", callback_data="start",
                         icon_custom_emoji_id=ICON_BACK),
             make_button(" ❌ ᴄʟᴏꜱᴇ ", callback_data="close",
                         icon_custom_emoji_id=ICON_CLOSE)]
        ])


def get_about_buttons():
    if BUTTON_STYLE_SUPPORTED:
        S = ButtonStyle
        return InlineKeyboardMarkup([
            [make_button(" 👨‍💻 ᴏᴡɴᴇʀ ", url="https://t.me/anujedits76",
                         icon_custom_emoji_id=ICON_DEV, style=S.PRIMARY)],
            [make_button(" ⬅️ ʙᴀᴄᴋ ", callback_data="start",
                         icon_custom_emoji_id=ICON_BACK, style=S.PRIMARY)]
        ])
    else:
        return InlineKeyboardMarkup([
            [make_button(" 👨‍💻 ᴏᴡɴᴇʀ ", url="https://t.me/anujedits76",
                         icon_custom_emoji_id=ICON_DEV)],
            [make_button(" ⬅️ ʙᴀᴄᴋ ", callback_data="start",
                         icon_custom_emoji_id=ICON_BACK)]
        ])


def get_start_buttons_cb():
    from .commands import get_start_buttons
    return get_start_buttons()


@Client.on_callback_query()
async def callback_query_handler(client, query: CallbackQuery):
    if query.data == "start":
        photo_url = await fetch_random_image()
        await query.message.edit_media(
            InputMediaPhoto(
                media=photo_url,
                caption=text.START.format(query.from_user.mention)
            ),
            reply_markup=get_start_buttons_cb()
        )

    elif query.data == "help":
        photo_url = await fetch_random_image()
        await query.message.edit_media(
            InputMediaPhoto(
                media=photo_url,
                caption=text.HELP
            ),
            reply_markup=get_help_buttons()
        )

    elif query.data == "about":
        photo_url = await fetch_random_image()
        await query.message.edit_media(
            InputMediaPhoto(
                media=photo_url,
                caption=text.ABOUT
            ),
            reply_markup=get_about_buttons()
        )

    elif query.data == "close":
        await query.message.delete()
