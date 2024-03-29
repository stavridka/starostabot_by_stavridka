from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery,FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from config import bot
from aiogram.types.input_file import FSInputFile

       
import os        
import keybs
import config
import DB
from datetime import date,datetime

router = Router()

class Form(StatesGroup):
    tg_id = State()
    


    

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
        send_data = DB.create_dict()
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
        

@router.callback_query(F.data == "go_to_db")
async def go_to_db(callback:CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Здесь можно прикоснуться к БД...', reply_markup=keybs.create_db_rule_kb())


@router.callback_query(F.data == "drop_day_code")
async def drop_day_code(callback:CallbackQuery):
    DB.drop_day_code()
    await callback.answer('Код посещения успешно сброшен!', show_alert=True)


@router.callback_query(F.data == "create_db_image")
async def create_db_image(callback:CallbackQuery):
    DB.create_tab1_image()
    doc = FSInputFile(config.tab_names[0])
    await bot.send_document(callback.from_user.id,doc)
    

@router.callback_query(F.data == "delete_student")
async def get_stud_id(callback:CallbackQuery, state:FSMContext):
    await callback.answer('Введите id, который необходимо удалить', show_alert=True)
    await state.set_state(Form.tg_id)
    

@router.message(Form.tg_id)
async def delete_student(msg:Message):
    DB.delete_student(msg.text)
    await msg.answer('Запись успешно удалена!', show_alert=True)
    
