import random
import re
import asyncio
import aiohttp
from asyncio import sleep
from .fonts import Fonts
from collections import defaultdict
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid, InputUserDeactivated
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import *
from Script import text
from .database import tb

try:
    from pyrogram.enums import ButtonStyle
    BUTTON_STYLE_SUPPORTED = True
except ImportError:
    BUTTON_STYLE_SUPPORTED = False

# =========================================================
# Button Icon Emoji IDs
# =========================================================
ICON_INFO    = 5334544901428229844
ICON_HELP    = 5443038326535759644
ICON_DEV     = 5823268688874179761
ICON_BACK    = 5447183459602669338
ICON_CLOSE   = 5210952531676504517
ICON_CHANNEL = 5271604874419647061
ICON_FEEDBACK= 5325547803936572038

def make_button(text_label, callback_data=None, url=None,
                icon_custom_emoji_id=None, style=None):
    kwargs = {"text": text_label}
    if callback_data:
        kwargs["callback_data"] = callback_data
    if url:
        kwargs["url"] = url
    if BUTTON_STYLE_SUPPORTED:
        if icon_custom_emoji_id:
            kwargs["icon_custom_emoji_id"] = icon_custom_emoji_id
        if style is not None:
            kwargs["style"] = style
    return InlineKeyboardButton(**kwargs)


def get_start_buttons():
    if BUTTON_STYLE_SUPPORTED:
        S = ButtonStyle
        return InlineKeyboardMarkup([
            [
                make_button(" ℹ️ ᴀʙᴏᴜᴛ ", callback_data="about",
                            icon_custom_emoji_id=ICON_INFO, style=S.PRIMARY),
                make_button(" 📚 ʜᴇʟᴘ ", callback_data="help",
                            icon_custom_emoji_id=ICON_HELP, style=S.PRIMARY),
            ],
            [
                make_button(" 💬 ꜰᴇᴇᴅʙᴀᴄᴋ 💬", url="https://telegram.me/anujedits76",
                            icon_custom_emoji_id=ICON_FEEDBACK, style=S.PRIMARY),
            ]
        ])
    else:
        return InlineKeyboardMarkup([
            [
                make_button(" ℹ️ ᴀʙᴏᴜᴛ ", callback_data="about",
                            icon_custom_emoji_id=ICON_INFO),
                make_button(" 📚 ʜᴇʟᴘ ", callback_data="help",
                            icon_custom_emoji_id=ICON_HELP),
            ],
            [
                make_button(" 💬 ꜰᴇᴇᴅʙᴀᴄᴋ 💬", url="https://telegram.me/anujedits76",
                            icon_custom_emoji_id=ICON_FEEDBACK),
            ]
        ])

# =========================================================
# Wallhaven Image Fetcher — ANIME + PEOPLE ONLY
# =========================================================

WALLHAVEN_API_KEY = "FsXt5pwoerVZrsV3DwhRctls8YzUev9H"

WALLHAVEN_QUERIES = [
    "anime+girl+portrait", "anime+portrait+face", "anime+girl+close+up",
    "anime+beautiful+face", "anime+school+girl", "anime+school+uniform",
    "anime+sailor+uniform", "anime+fantasy+girl", "anime+magic+girl",
    "anime+witch+girl", "anime+elf+girl", "anime+princess",
    "anime+dark+girl", "anime+gothic+girl", "anime+demon+girl",
    "anime+vampire+girl", "anime+girl+sakura", "anime+girl+nature",
    "anime+girl+sunset", "anime+girl+rain", "anime+girl+snow",
    "anime+girl+flowers", "anime+girl+forest", "anime+girl+summer",
    "anime+girl+winter", "anime+girl+spring", "anime+girl+autumn",
    "anime+kawaii+girl", "anime+cute+girl", "anime+chibi+girl",
    "anime+warrior+girl", "anime+sword+girl", "anime+ninja+girl",
    "anime+knight+girl", "anime+cyberpunk+girl", "anime+girl+ocean",
    "anime+girl+sky", "anime+girl+clouds", "anime+mermaid",
    "anime+girl+night", "anime+girl+stars", "anime+girl+moon",
    "anime+girl+galaxy", "anime+pink+hair+girl", "anime+blue+hair+girl",
    "anime+white+hair+girl", "anime+silver+hair+girl", "anime+red+hair+girl",
    "anime+blonde+anime+girl", "anime+girl+smile", "anime+girl+serious",
    "anime+kimono+girl", "anime+yukata+girl", "anime+shrine+maiden",
    "anime+japanese+girl", "anime+waifu", "anime+girl+4k",
    "anime+girl+aesthetic", "anime+girl+minimal", "anime+cherry+blossom",
    "anime+boy+cool", "anime+couple", "anime+art",
    "beautiful+girl+portrait", "asian+girl+portrait+4k",
    "aesthetic+girl+photography", "beautiful+woman+4k",
    "girl+nature+portrait", "model+photography+portrait",
    "cute+girl+wallpaper", "pretty+girl+face+portrait",
    "girl+sunset+photography", "woman+aesthetic+wallpaper",
    "girl+flowers+photography", "beautiful+eyes+portrait",
    "girl+rain+photography", "woman+forest+portrait",
    "girl+city+night+photography",
]


async def fetch_random_image() -> str:
    fallback = "https://wallhaven.cc/w/ex9gj7"
    try:
        query = random.choice(WALLHAVEN_QUERIES)
        page  = random.randint(1, 3)
        url = (
            f"https://wallhaven.cc/api/v1/search"
            f"?categories=011&purity=100&q={query}"
            f"&sorting=random&page={page}&apikey={WALLHAVEN_API_KEY}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                resp.raise_for_status()
                data = await resp.json()
                images = data.get("data", [])
                if not images:
                    url_fallback = (
                        f"https://wallhaven.cc/api/v1/search"
                        f"?categories=011&purity=100&sorting=random&apikey={WALLHAVEN_API_KEY}"
                    )
                    async with session.get(url_fallback, timeout=aiohttp.ClientTimeout(total=10)) as resp2:
                        data2 = await resp2.json()
                        images = data2.get("data", [])
                if not images:
                    return fallback
                chosen    = random.choice(images)
                image_url = chosen.get("path", fallback)
                return image_url
    except Exception as e:
        print(f"Wallhaven fetch failed: {e}")
        return fallback

FONT_STYLES = [
    Fonts.typewriter,
    Fonts.outline,
    Fonts.serif,
    Fonts.bold_cool,
    Fonts.cool,
    Fonts.smallcap,
    Fonts.script,
    Fonts.bold_script,
    Fonts.tiny,
    Fonts.comic,
    Fonts.sans,
    Fonts.slant_san,
    Fonts.slant,
    Fonts.sim,
    Fonts.circles,
    Fonts.dark_circle,
    Fonts.gothic,
    Fonts.bold_gothic,
    Fonts.cloud,
    Fonts.happy,
    Fonts.sad,
    Fonts.special,
    Fonts.square,
    Fonts.dark_square,
    Fonts.andalucia,
    Fonts.manga,
    Fonts.stinky,
    Fonts.bubbles,
    Fonts.underline,
    Fonts.ladybug,
    Fonts.rays,
    Fonts.birds,
    Fonts.slash,
    Fonts.stop,
    Fonts.skyline,
    Fonts.arrows,
    Fonts.rvnes,
    Fonts.strike,
    Fonts.frozen,
    Fonts.vaporwave,
    Fonts.cursive,
    Fonts.bold_cursive,
    Fonts.italic,
    Fonts.bold_italic,
    Fonts.fire,
    Fonts.royal,
    Fonts.double_struck,
    Fonts.glitch,
    Fonts.neon,
    Fonts.matrix,
    Fonts.medieval,
    Fonts.bold_medieval,
    Fonts.superscript,
    Fonts.subscript,
    Fonts.inverted,
    Fonts.mirror,
    Fonts.wavy,
    Fonts.diamond,
    Fonts.star_vip,
    Fonts.crown,
    Fonts.fancy_bold,
    Fonts.wiggly,
    Fonts.aesthetic,
    Fonts.lightning,
    Fonts.heart_vip,
    Fonts.sparkle,
    Fonts.dotted,
    # ✍️ Signature / Handwriting
    Fonts.signature,
    Fonts.ink_sign,
    Fonts.calligraphy,
    Fonts.handwrite,
    Fonts.pen_flow,
    Fonts.quill,
    Fonts.wedding,
    Fonts.cursive_bold_sign,
    # 🎮 Gaming / Futuristic
    Fonts.cyber,
    Fonts.hacker,
    Fonts.sci_fi,
    Fonts.pixel,
    Fonts.runic,
    Fonts.alien,
    Fonts.tech_square,
    Fonts.retrowave,
    Fonts.mech,
    Fonts.game_bold,
    Fonts.synthwave,
    Fonts.rpg,
    Fonts.space,
    # 🆕 NickFinder New Pack
    Fonts.fat_text,
    Fonts.inverted_square,
    Fonts.tribal,
    Fonts.illuminati,
    Fonts.crazy_mix,
    Fonts.luni_symbols,
    Fonts.wings,
    Fonts.heart_box,
    Fonts.star_box,
    Fonts.fancy_comma,
    Fonts.dotted_circle,
    Fonts.cross_style,
    Fonts.gamer,
    Fonts.bubble_pop,
    Fonts.fire_glow,
    Fonts.ninja,
    Fonts.chinese_style,
    Fonts.double_line,
    Fonts.tilted,
    # 🎮 Gaming Pack
    Fonts.pubg,
    Fonts.free_fire,
    Fonts.dragon,
    Fonts.demon,
    Fonts.neon_glitch,
    Fonts.matrix_rain,
    Fonts.skull,
    Fonts.leet,
    Fonts.warlord,
    Fonts.shadow,
    Fonts.blood,
    Fonts.thunder,
    Fonts.beast_mode,
    # 🎨 Decoration / Prefix-Suffix Pack
    Fonts.deco_star_katana,
    Fonts.deco_swirl_om,
    Fonts.deco_swirl_wave,
    Fonts.deco_cross_fat,
    Fonts.deco_checker_box,
    Fonts.deco_cyrillic_dots,
    Fonts.deco_cute_bow,
    Fonts.deco_cute_simple,
    Fonts.deco_arrow_bow,
    Fonts.deco_star_cute,
    Fonts.deco_mouse_cute,
    Fonts.deco_symbol_line,
    Fonts.deco_crazy1,
    Fonts.deco_crazy2,
    Fonts.deco_crazy3,
    Fonts.deco_crazy4,
    Fonts.deco_eye_of_ra,
    Fonts.deco_gun_style,
    Fonts.deco_gaming_star,
    Fonts.deco_crown_gaming,
    Fonts.deco_fire_gaming,
    Fonts.deco_sword,
    Fonts.deco_skull_gaming,
    Fonts.deco_devil,
    Fonts.deco_vip,
    Fonts.deco_pro,
    Fonts.deco_elegant1,
    Fonts.deco_elegant2,
    Fonts.deco_mixed_caps,
    # 🏆 NickFinder Popular Styles Pack
    Fonts.nick_swirl_wheel,
    Fonts.nick_heart_circle,
    Fonts.nick_mr_x,
    Fonts.nick_ak_boss,
    Fonts.nick_devil_mask,
    Fonts.nick_crown_swirl,
    Fonts.nick_the_korean,
    Fonts.nick_spaced,
    Fonts.nick_triangle_bracket,
    Fonts.nick_diamond_xx,
    Fonts.nick_ff_tick,
    Fonts.nick_ind_007,
    Fonts.nick_spade_heart,
    Fonts.nick_dot_spaced,
    Fonts.nick_arrow_fire,
    Fonts.nick_tm_ticks,
    Fonts.nick_blue_heart,
    Fonts.nick_wing_smile,
    Fonts.nick_double_pipe,
    Fonts.nick_circle_letters,
    Fonts.nick_dashed_box,
    Fonts.nick_swirl_star_border,
    Fonts.nick_lord_star,
    Fonts.nick_xx_border,
    Fonts.nick_cross_dagger,
    Fonts.nick_royal_check,
    Fonts.nick_flower_border,
    Fonts.nick_yin_yang,
    Fonts.nick_wave_star,
    Fonts.nick_ind_style,
    Fonts.nick_smily_face,
    Fonts.nick_devil_eye,
    Fonts.nick_tilde_style,
    Fonts.nick_quotes_border,
    Fonts.nick_angel_wing,
    Fonts.nick_danger_x,
    Fonts.nick_lone_bracket,
    Fonts.nick_teddy,
    Fonts.nick_shuriken,
    Fonts.nick_nail_teddy,
    Fonts.nick_king_bhai,
    Fonts.nick_hatch_border,
    Fonts.nick_op_boss,
    Fonts.nick_royal_anuj,
    Fonts.nick_swirl_anuj_star,
    Fonts.nick_star_katana_bracket,
    Fonts.nick_devil_smile,
    Fonts.nick_official_fire,
    Fonts.nick_heart_red,
    Fonts.nick_gaming_title,
    Fonts.nick_ff_style,
    Fonts.nick_mafia,
    Fonts.nick_underscore_spaced,
    Fonts.nick_check_border,
    Fonts.nick_tilde_underbar,
    Fonts.nick_swirl_wave_star,
    Fonts.nick_smoking,
    Fonts.nick_cross_tick,
    Fonts.nick_yin_devil,
    # 👑 VIP STYLES
    Fonts.vip_diamond,
    Fonts.vip_crown_gold,
    Fonts.vip_elite,
    Fonts.vip_legend,
    Fonts.vip_royal_star,
    Fonts.vip_boss,
    Fonts.vip_op,
    Fonts.vip_star_glow,
    Fonts.vip_toxic,
    Fonts.vip_godlike,
    # 🎮 FF / PUBG POPULAR STYLES
    Fonts.ff_booyah,
    Fonts.ff_headshot,
    Fonts.ff_pro_player,
    Fonts.ff_rank_master,
    Fonts.ff_squad,
    Fonts.ff_no_scope,
    Fonts.pubg_chicken_dinner,
    Fonts.pubg_conqueror,
    Fonts.pubg_ace,
    Fonts.pubg_sniper,
    # 💫 EMOJI BORDER STYLES
    Fonts.emoji_fire_border,
    Fonts.emoji_star_border,
    Fonts.emoji_lightning_border,
    Fonts.emoji_skull_border,
    Fonts.emoji_crown_border,
    Fonts.emoji_diamond_border,
    Fonts.emoji_sword_border,
    Fonts.emoji_gun_border,
    Fonts.emoji_devil_border,
    Fonts.emoji_angel_border,
    Fonts.emoji_dragon_border,
    Fonts.emoji_ninja_border,
    Fonts.emoji_trophy_border,
    Fonts.emoji_bomb_border,
    Fonts.emoji_target_border,
    # 🌈 COMBO POPULAR STYLES
    Fonts.popular_sweetheart,
    Fonts.popular_cool_fire,
    Fonts.popular_galaxy,
    Fonts.popular_demon_king,
    Fonts.popular_pro_sniper,
    Fonts.popular_shadow_wolf,
    Fonts.popular_angel_devil,
    Fonts.popular_ice_cold,
    Fonts.popular_blood_moon,
    Fonts.popular_thunder_god,
    Fonts.popular_dark_lord,
    Fonts.popular_toxic_vibes,
    # 🖼️ GAMING NICKNAME FRAME STYLES
    Fonts.frame_ff_rank,
    Fonts.frame_pubg_rank,
    Fonts.frame_vip_crown,
    Fonts.frame_hacker,
    Fonts.frame_demon_fire,
    Fonts.frame_legend,
    Fonts.frame_dragon_power,
    Fonts.frame_ninja_shadow,
    Fonts.frame_galaxy_star,
    Fonts.frame_toxic_skull,
    # 💫 MORE VIP CROWN STYLES
    Fonts.vip_queen,
    Fonts.vip_emperor,
    Fonts.vip_diamond2,
    Fonts.vip_neon_king,
    Fonts.vip_savage,
    Fonts.vip_alpha,
    Fonts.vip_omega,
    Fonts.vip_sigma,
    Fonts.vip_immortal,
    Fonts.vip_untouchable,
    Fonts.vip_ghost,
    Fonts.vip_titan,
    # 🎯 MORE FF STYLES
    Fonts.ff_legend,
    Fonts.ff_grandmaster,
    Fonts.ff_mythic,
    Fonts.ff_lone_wolf,
    Fonts.ff_rush_player,
    Fonts.ff_owner,
    Fonts.ff_clan_leader,
    Fonts.ff_killer,
    Fonts.ff_streamer,
    Fonts.ff_hacker_style,
    # 🪖 MORE PUBG STYLES
    Fonts.pubg_beryl,
    Fonts.pubg_groza,
    Fonts.pubg_zone_pusher,
    Fonts.pubg_last_circle,
    Fonts.pubg_hot_drop,
    Fonts.pubg_erangel,
    Fonts.pubg_miramar,
    Fonts.pubg_rush_mode,
    # 🌈 MORE EMOJI COMBO STYLES
    Fonts.combo_fire_skull,
    Fonts.combo_crown_fire,
    Fonts.combo_lightning_crown,
    Fonts.combo_sword_skull,
    Fonts.combo_star_diamond,
    Fonts.combo_moon_star,
    Fonts.combo_wolf_moon,
    Fonts.combo_snake_eye,
    Fonts.combo_robot_gear,
    Fonts.combo_alien_ufo,
    Fonts.combo_zombie,
    Fonts.combo_vampire,
    Fonts.combo_witch,
    Fonts.combo_pirate,
    Fonts.combo_samurai,
    Fonts.combo_viking,
    Fonts.combo_sniper_scope,
    Fonts.combo_grenade,
    Fonts.combo_phoenix,
    Fonts.combo_lion_king,
    # 🖼️ MORE NICKNAME FRAME STYLES
    Fonts.frame_royal_queen,
    Fonts.frame_fire_king,
    Fonts.frame_cyber_bot,
    Fonts.frame_ice_queen,
    Fonts.frame_death_note,
    Fonts.frame_thunder_lord,
    Fonts.frame_wolf_pack,
    Fonts.frame_toxic_gamer,
    Fonts.frame_samurai_fire,
    Fonts.frame_pro_gamer,
    Fonts.frame_shadow_king,
    Fonts.frame_neon_glow,
    Fonts.frame_beast_fire,
    Fonts.frame_ghost_skull,
    Fonts.frame_alien_tech,
    # 🎨 TRIPLE EMOJI BORDER STYLES
    Fonts.triple_fire,
    Fonts.triple_skull,
    Fonts.triple_crown,
    Fonts.triple_star,
    Fonts.triple_lightning,
    Fonts.triple_diamond,
    Fonts.triple_sword,
    Fonts.triple_devil,
    Fonts.triple_dragon,
    Fonts.triple_gun,
    # ✨ SPECIAL POPULAR NICKNAME STYLES
    Fonts.nick_yt_style,
    Fonts.nick_official,
    Fonts.nick_verified,
    Fonts.nick_pro_badge,
    Fonts.nick_no1,
    Fonts.nick_undefeated,
    Fonts.nick_impossible,
    Fonts.nick_solo_rank,
    Fonts.nick_top_fragger,
    Fonts.nick_ceo,
    Fonts.nick_gaming_god,
    Fonts.nick_beast,
    Fonts.nick_rage,
    Fonts.nick_clutch,
    Fonts.nick_sweaty,
    # 🎮 NEW VIP FF SYMBOL STYLES
    Fonts.ff_vip_zen,
    Fonts.ff_vip_x_blade,
    Fonts.ff_vip_mo,
    Fonts.ff_vip_san,
    Fonts.ff_vip_ogham,
    Fonts.ff_vip_sumerian,
    Fonts.ff_vip_swirl,
    Fonts.ff_vip_swirl_om,
    Fonts.ff_vip_bengali,
    Fonts.ff_vip_jp_bracket,
    Fonts.ff_vip_black_bracket,
    Fonts.ff_vip_math_bracket,
    Fonts.ff_vip_xbox,
    Fonts.ff_vip_god,
    Fonts.ff_vip_king_swirl,
    Fonts.ff_vip_boss_crown,
    Fonts.ff_vip_devil_swirl,
    Fonts.ff_vip_blood_swirl,
    Fonts.ff_vip_pro_star,
    Fonts.ff_vip_diamond_border,
    Fonts.ff_vip_zoro,
    Fonts.ff_vip_shadow_god,
    Fonts.ff_vip_toxic,
    Fonts.ff_vip_demon_king,
    Fonts.ff_vip_ninja_style,
    Fonts.ff_vip_ghost,
    Fonts.ff_vip_skull_king,
    Fonts.ff_vip_fire_lord,
    Fonts.ff_vip_ice_queen,
    Fonts.ff_vip_royal_v2,
    Fonts.ff_vip_alpha_wolf,
    Fonts.ff_vip_dragon_fire,
    Fonts.ff_vip_sniper_pro,
    Fonts.ff_vip_headshot,
    Fonts.ff_vip_booyah_king,
    Fonts.ff_vip_grandmaster,
    Fonts.ff_vip_legend_fire,
    # 🎮 PUBG VIP STYLES
    Fonts.pubg_vip_conqueror,
    Fonts.pubg_vip_ace_master,
    Fonts.pubg_vip_chicken,
    Fonts.pubg_vip_rush,
    Fonts.pubg_vip_pro,
    Fonts.pubg_vip_god,
    Fonts.pubg_vip_lone_wolf,
    Fonts.pubg_vip_commander,
    Fonts.pubg_vip_sniper,
    Fonts.pubg_vip_warlord,
    # 💎 SMALL CAPS VIP
    Fonts.vip_smallcap_god,
    Fonts.vip_smallcap_king,
    Fonts.vip_smallcap_devil,
    Fonts.vip_smallcap_boss,
    Fonts.vip_smallcap_shadow,
    # 🌟 TRENDING FF/PUBG 2025-26
    Fonts.trend_ff_clan,
    Fonts.trend_ff_op,
    Fonts.trend_ff_vip_style1,
    Fonts.trend_ff_vip_style2,
    Fonts.trend_ff_pro_style,
    Fonts.trend_ff_indian,
    Fonts.trend_ff_sweetheart,
    Fonts.trend_ff_hacker,
    Fonts.trend_ff_killer,
    Fonts.trend_ff_no_scope,
    Fonts.trend_pubg_erangel,
    Fonts.trend_pubg_hot_drop,
    Fonts.trend_ff_rank_push,
    Fonts.trend_ff_squad_leader,
    Fonts.trend_ff_owner,
    Fonts.trend_ff_big_boss,
    Fonts.trend_ff_untouchable,
    Fonts.trend_ff_mafia,
    Fonts.trend_ff_immortal,
    Fonts.trend_ff_mr_x,
    Fonts.trend_ff_sigma,
    Fonts.trend_ff_bloodbath,
    Fonts.trend_ff_ryze,
    Fonts.trend_ff_toxic_king,
]

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    if await tb.get_user(message.from_user.id) is None:
        await tb.add_user(message.from_user.id, message.from_user.first_name)
        bot = await client.get_me()
        await client.send_message(
            LOG_CHANNEL,
            text.LOG.format(
                message.from_user.id,
                getattr(message.from_user, "dc_id", "N/A"),
                message.from_user.first_name or "N/A",
                f"@{message.from_user.username}" if message.from_user.username else "N/A",
                bot.username
            )
        )
    photo_url = await fetch_random_image()
    await message.reply_photo(
        photo=photo_url,
        caption=text.START.format(message.from_user.mention),
        reply_markup=get_start_buttons()
    )

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):
    photo_url = await fetch_random_image()
    if BUTTON_STYLE_SUPPORTED:
        S = ButtonStyle
        buttons = InlineKeyboardMarkup([
            [make_button(" 📢 ᴜᴘᴅᴀᴛᴇꜱ ", url="https://telegram.me/anujedits76",
                         icon_custom_emoji_id=ICON_CHANNEL, style=S.PRIMARY)],
            [make_button(" ❌ ᴄʟᴏꜱᴇ ", callback_data="close",
                         icon_custom_emoji_id=ICON_CLOSE, style=S.DANGER)]
        ])
    else:
        buttons = InlineKeyboardMarkup([
            [make_button(" 📢 ᴜᴘᴅᴀᴛᴇꜱ ", url="https://telegram.me/anujedits76",
                         icon_custom_emoji_id=ICON_CHANNEL)],
            [make_button(" ❌ ᴄʟᴏꜱᴇ ", callback_data="close",
                         icon_custom_emoji_id=ICON_CLOSE)]
        ])
    await message.reply_photo(
        photo=photo_url,
        caption=text.HELP,
        reply_markup=buttons
    )


@Client.on_message(filters.command("about") & filters.private)
async def about_cmd(client, message):
    photo_url = await fetch_random_image()
    if BUTTON_STYLE_SUPPORTED:
        S = ButtonStyle
        buttons = InlineKeyboardMarkup([
            [make_button(" 👨‍💻 ᴏᴡɴᴇʀ ", url="https://t.me/anujedits76",
                         icon_custom_emoji_id=ICON_DEV, style=S.PRIMARY)],
            [make_button(" ❌ ᴄʟᴏꜱᴇ ", callback_data="close",
                         icon_custom_emoji_id=ICON_CLOSE, style=S.DANGER)]
        ])
    else:
        buttons = InlineKeyboardMarkup([
            [make_button(" 👨‍💻 ᴏᴡɴᴇʀ ", url="https://t.me/anujedits76",
                         icon_custom_emoji_id=ICON_DEV)],
            [make_button(" ❌ ᴄʟᴏꜱᴇ ", callback_data="close",
                         icon_custom_emoji_id=ICON_CLOSE)]
        ])
    await message.reply_photo(
        photo=photo_url,
        caption=text.ABOUT,
        reply_markup=buttons
    )


def parse_button_markup(text: str):
    lines = text.split("\n")
    buttons = []
    final_text_lines = []
    for line in lines:
        row = []
        parts = line.split("||")
        is_button_line = True
        for part in parts:
            match = re.fullmatch(r"\[(.+?)\]\((https?://[^\s]+)\)", part.strip())
            if match:
                row.append(InlineKeyboardButton(match[1], url=match[2]))
            else:
                is_button_line = False
                break
        if is_button_line and row:
            buttons.append(row)
        else:
            final_text_lines.append(line)
    return InlineKeyboardMarkup(buttons) if buttons else None, "\n".join(final_text_lines).strip()

@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMIN))
async def total_users(client: Client, message: Message):
    try:
        users = await tb.get_all_users()
        if BUTTON_STYLE_SUPPORTED:
            btn = InlineKeyboardMarkup([[make_button(" ❌ ᴄʟᴏꜱᴇ ", callback_data="close",
                icon_custom_emoji_id=ICON_CLOSE, style=ButtonStyle.DANGER)]])
        else:
            btn = InlineKeyboardMarkup([[make_button(" ❌ ᴄʟᴏꜱᴇ ", callback_data="close",
                icon_custom_emoji_id=ICON_CLOSE)]])
        await message.reply_text(
            f"<b>👥 ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ : <code>{len(users)}</code></b>",
            reply_markup=btn,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        r = await message.reply(f"❌ <code>{str(e)}</code>", parse_mode=enums.ParseMode.HTML)
        await asyncio.sleep(30)
        await r.delete()

@Client.on_message(filters.command("broadcast") & filters.private & filters.user(ADMIN))
async def broadcasting_func(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("<b>Reply to a message to broadcast.</b>", parse_mode=enums.ParseMode.HTML)
    msg = await message.reply_text("📢 Starting broadcast...")
    to_copy_msg = message.reply_to_message
    users_list = await tb.get_all_users()
    total_before = len(users_list)
    completed_users = set()
    failed = 0
    raw_text = to_copy_msg.caption or to_copy_msg.text or ""
    reply_markup, cleaned_text = parse_button_markup(raw_text)

    for i, user in enumerate(users_list, start=1):
        user_id = user.get("user_id")
        if not user_id:
            if await tb.delete_user(user.get("_id")):
                failed += 1
            continue
        try:
            user_id = int(user_id)  # normalize to int
            if to_copy_msg.text:
                await client.send_message(user_id, cleaned_text, reply_markup=reply_markup)
            elif to_copy_msg.photo:
                await client.send_photo(user_id, to_copy_msg.photo.file_id, caption=cleaned_text, reply_markup=reply_markup)
            elif to_copy_msg.video:
                await client.send_video(user_id, to_copy_msg.video.file_id, caption=cleaned_text, reply_markup=reply_markup)
            elif to_copy_msg.document:
                await client.send_document(user_id, to_copy_msg.document.file_id, caption=cleaned_text, reply_markup=reply_markup)
            else:
                await to_copy_msg.copy(user_id)

            completed_users.add(user_id)

        except (UserIsBlocked, PeerIdInvalid, InputUserDeactivated):
            if await tb.delete_user(user_id):
                failed += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await to_copy_msg.copy(user_id)
                completed_users.add(user_id)
            except Exception:
                if await tb.delete_user(user_id):
                    failed += 1
        except Exception:
            if await tb.delete_user(user_id):
                failed += 1
        if i % 20 == 0 or i == total_before:
            try:
                await msg.edit(
                    f"😶‍🌫 Broadcasting...\n\n"
                    f"👥 Total Users: {total_before}\n"
                    f"✅ Successful: <code>{len(completed_users)}</code>\n"
                    f"❌ Failed/Removed: <code>{failed}</code>\n"
                    f"⚙️ Progress: {i}/{total_before}"
                )
            except Exception:
                pass

        await asyncio.sleep(0.05)

    all_users = await tb.get_all_users()
    users_by_id = defaultdict(list)
    for user in all_users:
        uid = user.get("user_id")
        if not uid:
            if await tb.delete_user(user.get("_id")):
                failed += 1
            continue
        users_by_id[uid].append(user)

    for uid, docs in users_by_id.items():
        if uid in completed_users:
            for duplicate in docs[1:]:
                if await tb.delete_user(duplicate.get("user_id")):
                    failed += 1
        else:
            for doc in docs:
                if await tb.delete_user(doc.get("user_id")):
                    failed += 1

    active_users = len(completed_users)

    await msg.edit(
        f"🎯 <b>Broadcast Completed</b>\n\n"
        f"👥 Total Users (Before): <code>{total_before}</code>\n"
        f"✅ Successful: <code>{len(completed_users)}</code>\n"
        f"❌ Failed/Removed: <code>{failed}</code>\n"
        f"📊 Active Users (Now): <code>{active_users}</code>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 Close", callback_data="close")]]),
        )

@Client.on_message(filters.text & filters.private & ~filters.regex(r"^/"))
async def send_styled_fonts(client: Client, message: Message):
    if await tb.get_user(message.from_user.id) is None:
        await tb.add_user(message.from_user.id, message.from_user.first_name)
        bot = await client.get_me()
        try:
            await client.send_message(
                LOG_CHANNEL,
                text.LOG.format(
                    message.from_user.id,
                    getattr(message.from_user, "dc_id", "N/A"),
                    message.from_user.first_name or "N/A",
                    f"@{message.from_user.username}" if message.from_user.username else "N/A",
                    bot.username
                )
            )
        except:
            pass
    user_text = message.text
    for font_func in FONT_STYLES:
        try:
            styled_text = font_func(user_text)
            await client.send_message(
                chat_id=message.chat.id,
                text=styled_text,
                parse_mode=None
            )
            await sleep(0.2)
        except Exception as e:
            print(f"Error with {font_func.__name__}: {e}")
