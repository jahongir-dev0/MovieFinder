from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.admin_states import AddMovie
import json
import os
from data.config import ADMINS

# JSON fayl manzili
MOVIES_FILE = os.path.join('data', 'movies.json')

# Admin buyruqni boshlash
@dp.message_handler(Command("add_movie"), state=None)
async def add_movie_start(message: types.Message):
    # Faqat adminlar uchun tekshirish
    if str(message.from_user.id) not in ADMINS:
        await message.answer("⛔ Siz admin emassiz. Ushbu buyruq faqat adminlar uchun mavjud.")
        return

    # Adminni davlatga o'tkazish
    await message.answer("Kino faylini (video) yuboring:")
    await AddMovie.WaitingForMovie.set()

# Step 1: Kino faylini qabul qilish
@dp.message_handler(content_types=types.ContentType.VIDEO, state=AddMovie.WaitingForMovie)
async def add_movie_video(message: types.Message, state: FSMContext):
    await state.update_data(file_id=message.video.file_id)
    await message.answer("🎬 Kino nomini kiriting:")
    await AddMovie.WaitingForName.set()

# Step 2: Kino nomini qabul qilish
@dp.message_handler(state=AddMovie.WaitingForName)
async def add_movie_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🇺🇿 Kino tilini kiriting:")
    await AddMovie.WaitingForLanguage.set()

# Step 3: Kino tilini qabul qilish
@dp.message_handler(state=AddMovie.WaitingForLanguage)
async def add_movie_language(message: types.Message, state: FSMContext):
    await state.update_data(language=message.text)
    await message.answer("📀 Kino sifatini kiriting (masalan: HD, FullHD):")
    await AddMovie.WaitingForQuality.set()

# Step 4: Kino sifatini qabul qilish
@dp.message_handler(state=AddMovie.WaitingForQuality)
async def add_movie_quality(message: types.Message, state: FSMContext):
    await state.update_data(quality=message.text)
    await message.answer("🌏 Kino davlatini kiriting:")
    await AddMovie.WaitingForCountry.set()

# Step 5: Kino davlatini qabul qilish
@dp.message_handler(state=AddMovie.WaitingForCountry)
async def add_movie_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await message.answer("📆 Kino yili (faqat raqam) kiriting:")
    await AddMovie.WaitingForYear.set()

# Step 6: Kino yilini qabul qilish (validatsiya)
@dp.message_handler(state=AddMovie.WaitingForYear)
async def add_movie_year(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("📆 Iltimos, yilni faqat raqam sifatida kiriting:")
        return
    await state.update_data(year=message.text)
    await message.answer("🎞️ Kino teglarini (vergul bilan) kiriting:")
    await AddMovie.WaitingForTags.set()

# Step 7: Kino teglarini qabul qilish va JSON saqlash
@dp.message_handler(state=AddMovie.WaitingForTags)
async def add_movie_tags(message: types.Message, state: FSMContext):
    tags = [tag.strip().lower() for tag in message.text.split(",")]
    movie_data = await state.get_data()
    movie_data["tags"] = tags

    # JSON Faylga yozish
    try:
        # Fayl mavjudligini tekshirish va yaratish
        if not os.path.exists(MOVIES_FILE):
            with open(MOVIES_FILE, "w") as f:
                json.dump({"movies": []}, f)

        # JSON Faylni o'qish
        with open(MOVIES_FILE, "r") as f:
            data = json.load(f)

        # Yangi kino qo'shish
        movie_id = len(data["movies"]) + 1
        movie_data["id"] = movie_id
        data["movies"].append(movie_data)

        # JSON Faylni qayta yozish
        with open(MOVIES_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await message.answer(f"Kino muvaffaqiyatli qo'shildi. ID: {movie_id}")
    except Exception as e:
        await message.answer("Ma'lumotlarni saqlashda xatolik yuz berdi.")
        print(f"JSON saqlash xatosi: {e}")

    # Davlatni tugatish
    try:
        current_state = await state.get_state()
        if current_state:
            await state.finish()
            print("Davlat muvaffaqiyatli tugatildi.")
        else:
            print("Davlat allaqachon tugatilgan yoki mavjud emas.")
    except KeyError:
        print("Davlatni tugatishda KeyError yuz berdi. Foydalanuvchi allaqachon davlatdan chiqqan.")
    except Exception as e:
        print(f"Kutilmagan xato: {e}")