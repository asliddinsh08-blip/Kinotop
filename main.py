# main.py
# Telegram AI Kino Bot
# Python 3.11+

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)
from dotenv import load_dotenv
import asyncio
import os
import httpx
from bs4 import BeautifulSoup

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Language support
LANGUAGES = {
    "uz": {
        "welcome": "🎥 AI Kino Botga xush kelibsiz\n\n🔎 Video yoki Instagram link tashlang\nBot kinoni topadi",
        "webapp_button": "🎬 Kino App",
        "analyzing_video": "🔍 Video analiz qilinmoqda...",
        "movie_found": "🎬 Kino topildi",
        "movie_name": "📛 Nomi",
        "language": "🌍 Til",
        "download": "📥 Yuklab olish",
        "online": "▶️ Onlayn ko'rish",
        "movie_not_found": "Kino topilmadi. Iltimos, boshqa link yoki nom kiriting."
    },
    "ru": {
        "welcome": "🎥 Добро пожаловать в AI Кино Бот\n\n🔎 Отправьте ссылку на видео или Instagram\nБот найдет фильм",
        "webapp_button": "🎬 Кино Приложение",
        "analyzing_video": "🔍 Видео анализируется...",
        "movie_found": "🎬 Фильм найден",
        "movie_name": "📛 Название",
        "language": "🌍 Язык",
        "download": "📥 Скачать",
        "online": "▶️ Смотреть онлайн",
        "movie_not_found": "Фильм не найден."
    },
    "en": {
        "welcome": "🎥 Welcome to AI Movie Bot\n\n🔎 Send a video or Instagram link\nBot will find the movie",
        "webapp_button": "🎬 Movie App",
        "analyzing_video": "🔍 Analyzing video...",
        "movie_found": "🎬 Movie found",
        "movie_name": "📛 Name",
        "language": "🌍 Language",
        "download": "📥 Download",
        "online": "▶️ Watch Online",
        "movie_not_found": "Movie not found."
    }
}

user_language = "uz"

webapp = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎬 Kino App", web_app=WebAppInfo(url="https://your-miniapp.up.railway.app"))]],
    resize_keyboard=True
)

async def search_movie_tmdb(query: str):
    if not TMDB_API_KEY: return None
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language={user_language}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return data["results"][0] if data["results"] else None

@dp.message(Command("start"))
async def start(message: types.Message):
    lang = message.from_user.language_code if message.from_user.language_code in LANGUAGES else "uz"
    await message.answer(LANGUAGES[lang]["welcome"], reply_markup=webapp)

@dp.message()
async def kino_search(message: types.Message):
    lang = message.from_user.language_code if message.from_user.language_code in LANGUAGES else "uz"
    msg = message.text

    if "instagram.com" in msg or "tiktok.com" in msg:
        await message.answer(LANGUAGES[lang]["analyzing_video"])
        # Basic extraction logic
        movie_title_candidate = msg.split('/')[-2].replace('-', ' ') if '/' in msg else msg
        kino_data = await search_movie_tmdb(movie_title_candidate)
    else:
        kino_data = await search_movie_tmdb(msg)

    if kino_data:
        movie_name = kino_data.get("title")
        await message.answer(f"🎬 {LANGUAGES[lang]['movie_found']}\n\n📛 {movie_name}\n\n📥 Download: https://example.com/dl\n▶️ Online: https://example.com/watch")
    else:
        await message.answer(LANGUAGES[lang]["movie_not_found"])

async def main():
    print("BOT ISHLADI")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
