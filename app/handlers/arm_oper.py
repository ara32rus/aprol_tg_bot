import os
from enum import Enum

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.handlers import common
from app.db_manage.db import db_check, db_insert, db_fetchall, db_delete_by_id

class Order(StatesGroup):
    waiting_for_function = State()

async def get_url(message: types.Message, state: FSMContext):
    await state.finish()
    DB_NAME = os.getenv("DB_NAME")
    keyboard = types.ReplyKeyboardRemove()
    data = {}
    if db_check(DB_NAME):
        src_data = db_fetchall(DB_NAME, "distr", ['distrname', 'url'])
        for item in src_data:
            data[item[0]] = item[1]
    msg = ''
    for item in data:
        msg = msg + f"<b>{item}</b> - <i>{data[item]}</i>\n"
    #print(msg)
    await message.answer(msg, reply_markup=keyboard)
    await common.cmd_completed(message)

async def apr_cfg(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("cfg", reply_markup=keyboard)
    await common.cmd_completed(message)

async def cfg_yast(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("yast", reply_markup=keyboard)
    await common.cmd_completed(message)

async def cfg_touch(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("touch", reply_markup=keyboard)
    await common.cmd_completed(message)

async def install_update_suse(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("suse", reply_markup=keyboard)
    await common.cmd_completed(message)

async def cfg_ldap(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("ldap", reply_markup=keyboard)
    await common.cmd_completed(message)

async def cfg_locale(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("locale", reply_markup=keyboard)
    await common.cmd_completed(message)

async def cfg_na(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("na", reply_markup=keyboard)
    await common.cmd_completed(message)

async def cfg_secure(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("secure", reply_markup=keyboard)
    await common.cmd_completed(message)

async def cancel(message: types.Message, state: FSMContext):
    await common.cmd_cancel(message)

function_catalog = {
    "URL дистрибутивов" : get_url,
    "Настройка aprol config" : apr_cfg,
    "Настройка yast" : cfg_yast,
    "Настройка touchpad на панели САР" : cfg_touch,
    "Нстановка обновлений suse" : install_update_suse,
    "Настройка ldap" : cfg_ldap,
    "Локализация" : cfg_locale,
    "Настрока ПО Нефтеавтоматики" : cfg_na,
    "Настройка информационной безопасности" : cfg_secure,
    "Отмена" : cancel,
}


async def arm_oper_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in function_catalog:
        keyboard.add(name)
    await message.answer("Выберите требуемую информацию:", reply_markup=keyboard)
    await Order.waiting_for_function.set()

async def arm_oper_chosen(message: types.Message, state: FSMContext):
    if message.text not in function_catalog:
        await message.answer("Пожалуйста, выберите информацию используя клавиатуру ниже")
        return
    await function_catalog[message.text](message, state)



def register_handlers_arm_oper(dp: Dispatcher):
    dp.register_message_handler(arm_oper_start, commands="arm_oper", state="*")
    dp.register_message_handler(arm_oper_chosen, state=Order.waiting_for_function)
