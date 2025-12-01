import os
from pyrogram import Client, filters
from pyrogram.types import ChatAction
import requests
from bs4 import BeautifulSoup
from io import BytesIO

API_ID = int(os.environ.get("API_ID", "26047636"))
API_HASH = os.environ.get("API_HASH", "d8b1ed69ae1f937c5dd4d3cc8c8de440")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8388209429:AAGSHFmVDpZqryMYJur4FGYZAjUxWEe8VIk")
OWNER_ID = int(os.environ.get("OWNER_ID", "8367080346"))

app = Client("anime_thumb_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("thumb"))
def thumb(client, message):
    if len(message.command) < 2:
        message.reply_text("Please provide an anime name. Example:\n/thumb Naruto")
        return

    anime_name = " ".join(message.command[1:])
    search_url = f"https://anime-banner.onrender.com/?q={anime_name}"

    try:
        client.send_chat_action(message.chat.id, ChatAction.TYPING)
        r = requests.get(search_url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        img_tags = soup.find_all("img")
        if not img_tags:
            message.reply_text("No images found for this anime.")
            return

        for img_tag in img_tags[:3]:
            img_url = img_tag.get("src")
            if not img_url:
                continue
            if img_url.startswith("/"):
                img_url = "https://anime-banner.onrender.com" + img_url

            img_data = requests.get(img_url).content
            img_bytes = BytesIO(img_data)
            img_bytes.name = f"{anime_name}.jpg"
            message.reply_photo(photo=img_bytes, caption=f"Here is your image of {anime_name} 😎")

    except Exception as e:
        message.reply_text(f"Oops! Something went wrong:\n{e}")

app.run()
