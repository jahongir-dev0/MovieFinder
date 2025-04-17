from aiogram.dispatcher.filters.state import State, StatesGroup

class AddMovie(StatesGroup):
    WaitingForMovie = State()    # 🎥 Kino faylini kutish
    WaitingForName = State()     # 🎬 Kino nomini kutish
    WaitingForLanguage = State() # 🇺🇿 Kino tilini kutish
    WaitingForQuality = State()  # 📀 Kino sifatini kutish
    WaitingForCountry = State()  # 🌏 Kino davlatini kutish
    WaitingForYear = State()     # 📆 Kino yilini kutish
    WaitingForTags = State()     # 🎞️ Kino teglarini kutish
