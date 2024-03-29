from aiogram.types import ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config 

def create_notice_kb(date):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
    text = "Отметиться на парах",
    callback_data = f"notice_attendance{date}"))
    return builder.as_markup()


def create_admin_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
    text = "Начать сбор id в чате",
    callback_data = "start_collecting"))     
    builder.add(InlineKeyboardButton(
    text = "Начать отметку посещаемости",
    callback_data = "start_attendance"))
    builder.add(InlineKeyboardButton(
    text = "Завершить отметку посещаемости",
    callback_data = "stop_attendance"))    
    builder.add(InlineKeyboardButton(
    text = "DataBase",
    callback_data = "go_to_db"))         
    builder.adjust(1)
    return builder.as_markup()


def create_db_rule_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
    text = "Сброс кода посещения",
    callback_data = "drop_day_code")) 
    builder.add(InlineKeyboardButton(
    text = "Сформировать образ БД",
    callback_data = "create_db_image"))     
    builder.add(InlineKeyboardButton(
    text = "Удалить запись по id",
    callback_data = "delete_student"))       
    builder.adjust(1)
    return builder.as_markup()
    

def create_names_kb():
    builder = InlineKeyboardBuilder()
    for name in config.names:
        builder.button(text=name,callback_data=name.split()[0])
    builder.adjust(2)
    return builder.as_markup()


kb = create_names_kb()
admin_kb = create_admin_kb()

