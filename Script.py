E_CHECK  = '<emoji id=5206607081334906820>✔️</emoji>'
E_CROSS  = '<emoji id=5210952531676504517>❌</emoji>'
E_WARN   = '<emoji id=5447644880824181073>⚠️</emoji>'
E_BOLT   = '<emoji id=5456140674028019486>⚡️</emoji>'
E_ROCKET = '<emoji id=5456140674028019486>🚀</emoji>'
E_INFO   = '<emoji id=5334544901428229844>ℹ️</emoji>'
E_GEAR   = '<emoji id=5341715473882955310>⚙️</emoji>'
E_PENCIL = '<emoji id=5395444784611480792>✏️</emoji>'
E_STAR   = '<emoji id=5438496463044752972>⭐️</emoji>'
E_CROWN  = '<emoji id=5217822164362739968>👑</emoji>'
E_SPARK  = '<emoji id=5325547803936572038>✨</emoji>'
E_ARROW  = '<emoji id=5416117059207572332>➡️</emoji>'
E_DEV    = '<emoji id=5823268688874179761>👨‍💻</emoji>'
E_LINK   = '<emoji id=5271604874419647061>🔗</emoji>'
E_DIAMOND= '<emoji id=5217822164362739968>💎</emoji>'

class text(object):

    START = (
        f"<b>{E_STAR} {{0}},</b>\n"
        f"<b>{E_SPARK} ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ꜱᴛʏʟɪꜱʜ ꜰᴏɴᴛ ᴠɪᴘ ʙᴏᴛ</b>\n"
        f"<blockquote>"
        f"<b>{E_ARROW} ᴛʀᴀɴꜱꜰᴏʀᴍ ᴀɴʏ ᴛᴇxᴛ ɪɴᴛᴏ 431+ ᴘʀᴇᴍɪᴜᴍ ꜰᴏɴᴛ ꜱᴛʏʟᴇꜱ</b>\n"
        f"<b>{E_ARROW} ᴘᴇʀꜰᴇᴄᴛ ꜰᴏʀ ʙɪᴏꜱ, ᴜꜱᴇʀɴᴀᴍᴇꜱ, ᴄᴀᴘᴛɪᴏɴꜱ & ʙʀᴀɴᴅɪɴɢ</b>\n"
        f"<b>{E_ARROW} ɪɴꜱᴛᴀɴᴛ ʀᴇꜱᴜʟᴛꜱ ᴡɪᴛʜ ᴏɴᴇ ᴛᴀᴘ ᴄᴏᴘʏ</b>\n"
        f"<b>{E_ARROW} ꜰᴀꜱᴛ, ꜱᴇᴄᴜʀᴇ & ᴘʀᴇᴍɪᴜᴍ ᴇxᴘᴇʀɪᴇɴᴄᴇ</b>"
        f"</blockquote>\n"
        f"<i>{E_BOLT} ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴀɴʏ ᴛᴇxᴛ ᴀɴᴅ ɢᴇᴛ ɪᴛ ᴄᴏɴᴠᴇʀᴛᴇᴅ ɪɴꜱᴛᴀɴᴛʟʏ.</i>\n"
        f"<blockquote>{E_CROWN} ᴠɪᴘ ᴇᴅɪᴛɪᴏɴ • ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀɴᴜᴊ</blockquote>"
    )

    LOG = """🔥 ɴᴇᴡ ᴜꜱᴇʀ ᴅᴇᴛᴇᴄᴛᴇᴅ

◈ ɪᴅ : <code>{}</code>
◈ ᴅᴄ : {}
◈ ꜰɪʀꜱᴛ ɴᴀᴍᴇ : {}
◈ ᴜꜱᴇʀɴᴀᴍᴇ : @{}

⚡ ʀᴇꜰᴇʀʀᴇᴅ ʙʏ : @{}"""

    ABOUT = (
        f"<blockquote>{E_INFO} <b>💠 ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ 💠</b>\n\n"
        f"<b>╭────[ {E_SPARK} ᴀɴᴜᴊ ]────⍟</b>\n"
        f"<b>├⍟ {E_ROCKET} ʙᴏᴛ ɴᴀᴍᴇ : <a href='https://t.me/anujedits76'>ꜱᴛʏʟɪꜱʜ ꜰᴏɴᴛ ᴠɪᴘ</a></b>\n"
        f"<b>├⍟ {E_DEV} ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/anujedits76'>ᴀɴᴜᴊ ᴋᴜᴍᴀʀ</a></b>\n"
        f"<b>├⍟ {E_LINK} ʟɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>ᴘʏʀᴏɢʀᴀᴍ ᴀꜱʏɴᴄ</a></b>\n"
        f"<b>├⍟ {E_BOLT} ʟᴀɴɢᴜᴀɢᴇ : <a href='https://www.python.org/'>ᴘʏᴛʜᴏɴ 3.11+</a></b>\n"
        f"<b>├⍟ {E_GEAR} ᴅᴀᴛᴀʙᴀꜱᴇ : <a href='https://www.mongodb.com/'>ᴍᴏɴɢᴏᴅʙ</a></b>\n"
        f"<b>├⍟ {E_STAR} ʜᴏꜱᴛɪɴɢ : <a href='https://www.koyeb.com/'>ᴋᴏʏᴇʙ ᴄʟᴏᴜᴅ</a></b>\n"
        f"<b>├⍟ {E_DIAMOND} ᴠᴇʀꜱɪᴏɴ : ᴠɪᴘ ᴇᴅɪᴛɪᴏɴ</b>\n"
        f"<b>╰───────────────⍟</b></blockquote>\n"
    )

    HELP = (
        f"<b>{E_SPARK} ʜᴏᴡ ᴛᴏ ᴜꜱᴇ</b>\n\n"
        f"<blockquote><b>① {E_PENCIL} ꜱᴇɴᴅ ᴀɴʏ ᴛᴇxᴛ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ</b></blockquote>\n"
        f"<blockquote><b>② {E_STAR} ɢᴇᴛ 431+ ᴜɴɪQᴜᴇ ꜱᴛʏʟɪꜱʜ ꜰᴏɴᴛꜱ ɪɴꜱᴛᴀɴᴛʟʏ</b></blockquote>\n"
        f"<blockquote><b>③ {E_CHECK} ᴄᴏᴘʏ ᴀɴᴅ ᴜꜱᴇ ᴛʜᴇᴍ ᴏɴ:</b>\n"
        f"{E_ARROW} ɪɴꜱᴛᴀɢʀᴀᴍ\n"
        f"{E_ARROW} ᴡʜᴀᴛꜱᴀᴘᴘ\n"
        f"{E_ARROW} ᴛᴇʟᴇɢʀᴀᴍ\n"
        f"{E_ARROW} ᴅɪꜱᴄᴏʀᴅ\n"
        f"{E_ARROW} ꜰᴀᴄᴇʙᴏᴏᴋ\n"
        f"{E_ARROW} ɢᴀᴍɪɴɢ ᴘʀᴏꜰɪʟᴇꜱ</blockquote>\n\n"
        f"<blockquote>{E_WARN} ᴛʜɪꜱ ʙᴏᴛ ᴡᴏʀᴋꜱ ᴏɴʟʏ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ.</blockquote>\n"
        f"<blockquote>{E_CROWN} ᴠɪᴘ ᴘᴏᴡᴇʀᴇᴅ • ʙʏ ᴀɴᴜᴊ</blockquote>"
    )
