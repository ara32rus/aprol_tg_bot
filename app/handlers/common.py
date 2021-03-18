import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.handlers.arm_oper import arm_oper_start
from app.db_manage.db import db_check, db_insert, db_fetchall, db_delete_by_id


function_catalog = ["Настройка АРМ оператора", "Настройка АРМ инженера", "Отмена"]


class OrderCommon(StatesGroup):
    waiting_for_function = State()


async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in function_catalog:
        keyboard.add(name)
    await message.answer("Выберите требуемую информацию:", reply_markup=keyboard)
    await OrderCommon.waiting_for_function.set()


async def cmd_chosen(message: types.Message, state: FSMContext):
    if message.text not in function_catalog:
        await message.answer("Пожалуйста, выберите информацию используя клавиатуру ниже")
        return
    await state.finish()
    await arm_oper_start(message)

async def cmd_cancel(message: types.Message):
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())

async def cmd_completed(message: types.Message):
    await message.answer("Спасибо за использование нашего справочника!", reply_markup=types.ReplyKeyboardRemove())


# Просто функция, которая доступна только администратору,
# чей ID указан в файле конфигурации.
async def add_distr_url(message: types.Message):
    DB_NAME = os.getenv("DB_NAME")
    src_data = message.text.replace("/add_distr_url", ' ').strip(' ')
    data = []
    for item in src_data.split(' '):
        data.append(item.strip('\"'))
    if (len(data) == 2 ):
        if (db_check(DB_NAME)):
            data = {"distrname" : f"{data[0]}" , "url" : f"{data[1]}"}
            if type(data) == dict:
                db_insert(DB_NAME, "distr", data)
            else:
                await message.answer("Некорректно сформированы данные")
        else:
            await message.answer("Нет доступа к базе данных!")
            return
    else:
        await message.answer("Данные о дистрибутиве введены некорретно! Введите данные в формате \"name\" \"url\"!")
        return


def register_handlers_common(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_chosen, state=OrderCommon.waiting_for_function)
    dp.register_message_handler(add_distr_url, IDFilter(user_id=admin_id), commands="add_distr_url")
