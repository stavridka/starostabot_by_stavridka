from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from config import bot

import keybs
import config
import DB
from datetime import date,datetime
from config import MyCallBack

router = Router()

class RegisterMessages(StatesGroup):
    step1 = State()
    stap2 = State()


    

@router.message(Command("start"))
async def start(msg:Message,state:FSMContext):
    if msg.from_user.id in config.ADMIN_ID:
        await msg.answer('ПРиветствую админа! Чем обязан?',reply_markup=keybs.admin_kb)
        

@router.message(lambda message: message.text in config.names)
async def choose_name(msg:types.Message):
    await msg.reply(f'Вы - {msg.text} ')
    DB.insert_in_group(msg.from_user.id, msg.text, msg.from_user.username)


   
#callbacks_handlers

@router.callback_query(lambda c: "notice_attendance" in c.data)
async def notice_attendance(callback:CallbackQuery):
    if DB.get_student(callback.from_user.id) is not None:
        data = datetime.strftime(date.today(),'%Y-%m-%d')
        if (callback.data[17:] == data) and (DB.is_attendance_fin() == True):
            DB.add_attendance(callback.from_user.id)
            await callback.answer(f"Вы успешно отметились за {date.today()}!",show_alert=True)
        else:
            await callback.answer('Фиксация посещений на этот день уже завершена',show_alert=True)
    else:
        await callback.answer('В базе данных отсутствуют сведения о вашем профиле,обратитесь с администратору ',show_alert=True)

@router.callback_query(F.data == "start_collecting")
async def start_collecting(msg:Message):
    await bot.send_message(config.test_key, 'Выберите своё имя',reply_markup=keybs.kb)
    

@router.callback_query(F.data == "start_attendance")
async def start_attendance(msg:Message):
    if DB.is_attendance_fin() == True:
        await bot.send_message(config.test_key, 'v Отмечаться - тут v',reply_markup=keybs.create_notice_kb(date.today()))
    else:
        await msg.answer('Сегодня проверка посещаемости уже проведена!',show_alert=True)
    

@router.callback_query(F.data == "stop_attendance")
async def stop_attendance(msg:Message):
    if DB.is_attendance_fin() == True:
        await bot.send_message(config.test_key, f'Отметка посещаемости завершена, {DB.get_quantity()} студентов отмечено!')
        DB.new_day()
    else:
        await msg.answer('Сегодня вы уже заверяли посещаемость!',show_alert=True)


@router.callback_query(lambda c: c.data in config.surnames)
async def add_new_student(callback:CallbackQuery):
    c = callback.data
    full_name = ''
    for name in config.names:
        if c == name.split()[0]:
            full_name = name
              
    if DB.get_student(callback.from_user.id) is None and DB.is_name_available(full_name) is None:
        DB.insert_in_group(callback.from_user.id,full_name, callback.from_user.username)
        await callback.answer(f'Вы были добавлены в список группы как {full_name}', show_alert=True)
    else:
        await callback.answer('Это имя/ваш id уже записан в базу данных. Если вы не выбирали свое имя или выбрали чужое имя по ошибке, обратитесь к администратору.', show_alert=True)