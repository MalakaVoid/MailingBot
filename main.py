from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from db_controller import delete_group_from_database, delete_admin_from_database, add_group_to_database,add_admin_to_database, is_admin_here, get_chat_ids
from globals import TOKEN_API, group_title,group_chat_id, admins
from keyboards import get_inline_keyboard
from datetime import datetime, timedelta
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
#---Начальная настройка
bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot,
                storage=storage)
#---Класс состояний, enterMessage - для ожидания сообщений для рассылки
class ReplyST(StatesGroup):
    enterMessage = State()

@dp.message_handler(state=ReplyST.enterMessage, content_types=Text)
async def get_message_to_mail(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if is_admin_here(message.chat.username):
            await bot.send_message(message.chat.id,
                                   text=message.text,
                                   reply_markup=get_inline_keyboard('check_correctness_msg_ikb'))
            await state.finish()

@dp.message_handler(state=None)
async def get_message_of_group(message: types.Message):
    if message.chat.type == "group":
        if message.chat.title not in group_title and message.chat.id not in group_chat_id:
            await add_group_to_db(message.chat)

@dp.message_handler(commands=['start'])
async def start_btn_hndl(message: types.Message):
    if message.chat.type == "private":
        if is_admin_here(message.chat.username):
            await send_main_menu_mes(message.chat.id)

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('mm_btn'))
async def main_menu_ikb_hndl(callback: types.CallbackQuery):
    if callback.data == 'start_mailing_mm_btn':
        await callback.message.edit_text(text='Введите сообщение для рассылки',
                                         reply_markup=get_inline_keyboard('cancel_mailing_ikb'))
        await ReplyST.enterMessage.set()
    elif callback.data == 'mailings_groups_mm_btn':
        a=1
        #Функция для получения всех групп для рассылки
    elif callback.data == 'del_mailing_group_mm_btn':
        a=1
        #Функция для удаления группы из рассылки

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('c_btn'), state=ReplyST.enterMessage)
async def cancel_mailing_btn(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await send_main_menu_mes(callback.message.chat.id)
    await callback.message.delete_reply_markup()

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('c_btn'), state=None)
async def cancel_mailing_err_btn(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('c_btn'), state=None)
async def cancel_mailing_err_btn(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()

async def send_main_menu_mes(chat_id):
    await bot.send_message(chat_id=chat_id,
                           text="Выберите опцию:",
                           reply_markup=get_inline_keyboard('main_menu_ikb'))

async def add_group_to_db(chat_ex):
    group_title.append(chat_ex.title)
    group_chat_id.append(chat_ex.id)
    #Функция для добавления в бд



if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)

