from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ChatJoinRequest, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton, MediaGroup, \
    InputFile
import sqlite3
import sender

connect = sqlite3.connect('users.db')
cursor = connect.cursor()
sender.cursor = cursor

token = '6839694364:AAH9jqlGkiPa1oeJLZ_LlXVz8U6vZYAnNkM'
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
sender.set_bot(dp)
sender.init_handlers()

TEXT_APPROVE_USER = '''MEN KIMMAN❓HAMMAGA SALOM ✊ 

Mening ismim Sardor Karimov
Men 25 yoshdaman, Buhara shahrida tug'ilganman 🌆
Men sizga o'zim haqimda bir voqeani aytib bermoqchiman

Yaqinda men onlayn o'yinlarni o'ynashni boshladim, keyin bu sohaga kirib, jamoamni yaratdim. Mening jamoamda dasturchilar o'yinlarni buzishadi va har kuni 100% sxemalarni bajaradilar. Men siz bilan baham ko'rmoqchiman! 😡⚡️

100% SHEMA OLISH UCHUN BOTDA HAR QANDAY XABARNI YOZING'''

TEXT_LEAVE_USER = '''Do'stim, qara, nima etishmayapti. Men kuniga o'nlab odamlarga pul ishlashga yordam beraman! Siz 70 000 dan boshlashingiz mumkin va ikki soat ichida sizda 350 000 bo'ladi.

кнопка вниз со ссылкой на личку
Pul ishlashni boshlang'''
me_dog = 'https://t.me/sardor_cash'
CHANNEL_ID = -1001976592255

approve_keyboard = InlineKeyboardMarkup()
approve_keyboard.add(InlineKeyboardButton('MANGA YOZING', url=me_dog))

leave_keyboard = InlineKeyboardMarkup()
leave_keyboard.add(InlineKeyboardButton('Pul ishlashni boshlang', url=me_dog))


@dp.chat_join_request_handler(chat_id=CHANNEL_ID)
async def approve_user(update: ChatJoinRequest):
    try:
        cursor.execute("INSERT INTO USERS VALUES(?)", (update.from_user.id, ))
        connect.commit()
    except:
        pass

    await update.approve()
    await bot.send_photo(
        chat_id=update.from_user.id,
        photo=open('approved.png', 'rb').read(),
        caption=TEXT_APPROVE_USER,
        reply_markup=approve_keyboard
    )


@dp.chat_member_handler(chat_id=CHANNEL_ID)
async def leave_user(chat_member_updated: ChatMemberUpdated):
    if chat_member_updated.new_chat_member.status == 'left':
        media = MediaGroup()
        media.attach_photo(InputFile('leave1.png'))
        media.attach_photo(InputFile('leave2.png'))
        await bot.send_media_group(chat_id=chat_member_updated.from_user.id, media=media)
        await bot.send_message(
            chat_id=chat_member_updated.from_user.id,
            text=TEXT_LEAVE_USER,
            reply_markup=leave_keyboard
        )


executor.Executor(dp).start_polling(allowed_updates=["message", "inline_query", "chat_member", 'chat_join_request', 'callback_query'])
