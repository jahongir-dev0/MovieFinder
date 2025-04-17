from aiogram import types
from loader import dp
import json
import os
from keyboards.default.buttons import user_keyboard

# JSON fayl manzili
MOVIES_FILE = os.path.join('data', 'movies.json')

# Welcome message with user keyboard
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.answer(
        "Xush kelibsiz! Quyidagi tugmachalardan birini tanlang:",
        reply_markup=user_keyboard
    )

# Handle "🔍 Kino ID bo'yicha qidirish"
@dp.message_handler(lambda message: message.text == "🔍 Kino ID bo'yicha qidirish")
async def search_by_id_prompt(message: types.Message):
    await message.answer("Kino ID raqamini kiriting:")

# Handle "🎞️ Teg bo'yicha qidirish"
@dp.message_handler(lambda message: message.text == "🎞️ Teg bo'yicha qidirish")
async def search_by_tag_prompt(message: types.Message):
    await message.answer("Kinoning teglarini kiriting (vergul bilan):")

# Search by ID
@dp.message_handler(lambda message: message.text.isdigit())
async def search_movie_by_id(message: types.Message):
    movie_id = int(message.text)

    # Load movies
    if not os.path.exists(MOVIES_FILE):
        await message.answer("Hozircha kinolar yo'q.")
        return

    with open(MOVIES_FILE, "r") as f:
        data = json.load(f)

    movie = next((m for m in data["movies"] if m["id"] == movie_id), None)
    if movie:
        await message.answer_video(
            video=movie["file_id"],
            caption=(
                f"🎬 Nomi: {movie['name']}\n"
                f"🇺🇿 Tili: {movie['language']}\n"
                f"📀 Sifati: {movie['quality']}\n"
                f"🌏 Davlat: {movie['country']}\n"
                f"📆 Yili: {movie['year']}\n"
                f"🎞️ Teglari: {', '.join(movie['tags'])}"
            )
        )
    else:
        await message.answer("Berilgan ID bo'yicha kino topilmadi.")

# Search by tags
@dp.message_handler()
async def search_movie_by_tags(message: types.Message):
    search_tags = [tag.strip().lower() for tag in message.text.split(",")]

    # Load movies
    if not os.path.exists(MOVIES_FILE):
        await message.answer("Hozircha kinolar yo'q.")
        return

    with open(MOVIES_FILE, "r") as f:
        data = json.load(f)

    # Match To'gri kelsa
    matching_movies = []
    for movie in data["movies"]:
        movie_tags = [tag.lower() for tag in movie["tags"]]
        if any(tag in movie_tags for tag in search_tags):
            matching_movies.append(movie)

    if matching_movies:
        for movie in matching_movies:
            await message.answer_video(
                video=movie["file_id"],
                caption=(
                    f"🎬 Nomi: {movie['name']}\n"
                    f"🇺🇿 Tili: {movie['language']}\n"
                    f"📀 Sifati: {movie['quality']}\n"
                    f"🌏 Davlat: {movie['country']}\n"
                    f"📆 Yili: {movie['year']}\n"
                    f"🎞️ Teglari: {', '.join(movie['tags'])}"
                )
            )
    else:
        await message.answer("Berilgan teglar bo'yicha kinolar topilmadi.")