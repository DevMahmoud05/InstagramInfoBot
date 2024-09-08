import requests
import telebot
from telebot.types import InlineKeyboardButton as Btn, InlineKeyboardMarkup as Mak


def info(user):
    headers = {
        "referer": "https://storiesig.info/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }

    response = requests.get(
        f"https://api-ig.storiesig.info/api/userInfoByUsername/{user}", headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        user_info = data["result"]["user"]
        # Extracting required fields from user_info
        id = user_info["pk"]
        username = user_info["username"]
        full_name = user_info["full_name"]
        bio = user_info["biography"]
        followers = user_info["follower_count"]
        following = user_info["following_count"]
        media_count = user_info["media_count"]
        profile_pic_url = user_info["profile_pic_url"]
        external_url = user_info["external_url"]
        is_private = "Private" if user_info["is_private"] else "Public"
        is_business = "Yes" if user_info["is_business"] else "No"
        details = f"""
ID: {id}
Username: {username}
Full Name: {full_name}
Bio: {bio}
Followers: {followers}
Following: {following}
Media Posts: {media_count}
Account Status: {is_private}
Business Account: {is_business}
External Link: {external_url}
    """
        return details, profile_pic_url
    else:
        return None, None


token = "7490207684:AAFNSWN9F_daLTVHCJ0q-Lz76KR1EhA4h9o"
bot = telebot.TeleBot(token, num_threads=30, skip_pending=True)


@bot.message_handler(commands=["start"])
def Welcome(msg):
    name = f"[{msg.from_user.first_name}](tg://settings)"
    bot.reply_to(
        msg,
        f"Hello {name}, welcome to the Instagram Account Info Bot!\nSend Only username",
        parse_mode="markdown",
        reply_markup=Mak().add(Btn("Owner", url="dev_mahmoud_05.t.me")),
    )


@bot.message_handler(content_types=["text"])
def Info(m):
    user = m.text
    inf, img_url = info(user)

    bot.send_photo(
        m.chat.id,
        img_url,
        caption=inf,
        reply_to_message_id=m.message_id,
    )


@bot.inline_handler(lambda query: True)
def inline_query(query):
    user = query.query
    inf, img_url = info(user)

    us = bot.get_me().username
    results = [
        telebot.types.InlineQueryResultPhoto(
            id="1",
            photo_url=img_url,
            thumb_url=img_url,
            caption=inf,
            reply_markup=Mak().add(Btn("Your Account Info", url=f"{us}.t.me")),
        )
    ]

    bot.answer_inline_query(query.id, results=results)


bot.infinity_polling()
