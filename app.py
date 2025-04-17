from aiogram import executor
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.config import ADMINS

# Bot ishga tushganda bajariladigan ishlar
async def on_startup(dispatcher):
    # Birlamchi komandalar (/start va /help)
    await set_default_commands(dispatcher)

    # Adminlarga bot ishga tushgani haqida xabar
    for admin in ADMINS:
        try:
            await dispatcher.bot.send_message(
                admin,
                "Bot ishga tushdi! Siz endi /add_movie buyrug‘idan foydalanishingiz mumkin."
            )
        except Exception as err:
            print(f"Admin {admin} ga xabar yuborishda xatolik: {err}")

    # Adminga umumiy xabar jo'natish
    await on_startup_notify(dispatcher)

# Botni ishga tushirish
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)