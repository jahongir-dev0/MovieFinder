from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Foydalanuvchilar uchun tugmalar
search_movie_id_button = KeyboardButton("🔍 Kino ID bo'yicha qidirish")
search_movie_tag_button = KeyboardButton("🎞️ Teg bo'yicha qidirish")

user_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
user_keyboard.add(search_movie_id_button, search_movie_tag_button)