from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from globals import TOKEN_API, group_host, admins
from keyboards import get_unline_keyboard
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
#---handler - для сообщения для рассылки
@dp.message_handler(state=ReplyST.enterMessage)
async def get_message_to_reply(message: types.Message, state: FSMContext):
    str_report = await send_messages_to_groups(message.text)
    await state.finish()
    await bot.send_message(message.chat.id,
                           text=str_report,
                           reply_markup=get_unline_keyboard('5'))

#---handler для кнопок добавления группы в рассылку
@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('start_btn'))
async def ik_cb_start_handler(callback: types.CallbackQuery):
    if callback.data == 'add_group_to_reply_start_btn':
        await add_group_to_reply(callback.message.chat)
        await callback.message.edit_text(text="Группа успешно добавлена. Удалить данное сообщение?",
                                         reply_markup=get_unline_keyboard('2'))
    elif callback.data == 'no_add_group_to_reply_start_btn':
        await callback.message.edit_text(text="Удалить данное сообщение?",
                                         reply_markup=get_unline_keyboard('2'))

#---handler для кнопки удаления сообщение
@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('del_btn'))
async def ik_cb_del_btns_handler(callback: types.CallbackQuery):
    if callback.data == 'yes_del_btn':
        await callback.message.delete()

#---handler команды /start
@dp.message_handler(commands=['start'])
async def hello_msg(message: types.Message):
    if (message.chat.type=="group" and message.from_user.username in admins):
        await bot.send_message(message.chat.id,
                               text="Добавить группу в рассылку?",
                               reply_markup=get_unline_keyboard('1'))
    elif message.chat.type == "private" and message.chat.username in admins:
        await bot.send_message(message.chat.id,
                               text="Выберите опцию:",
                               reply_markup=get_unline_keyboard('3'))
    else:
        await bot.send_message(text="У вас нет доступа к этому боту!",
                               chat_id=message.chat.id)

#---handler для кнопок главного меню
@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('reply_btn'))
async def ik_cb_reply_btns_handler(callback: types.CallbackQuery):
    if callback.data == 'start_reply_btn':
        await ReplyST.enterMessage.set()
        await callback.message.edit_text(text="Введите сообщение для рассылки:",
                                         reply_markup=get_unline_keyboard('4'))
    elif callback.data == 'show_groups_reply_btn':
        str_res = await get_all_reply_groups()
        await callback.message.edit_text(text=str_res,
                                         reply_markup=get_unline_keyboard('5'))

#---handler кнопки отмена при вводе сообщения для рассылки
@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('cancel_btn'), state=ReplyST.enterMessage)
async def ik_cb_cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id,
                           text="Выберите опцию:",
                           reply_markup=get_unline_keyboard('3'))
    await state.finish()
    await callback.message.delete()

#---handler устаревшей кнопки отмены
@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('cancel_btn'), state=None)
async def ik_cb_cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

#---handler кнопки Назад при выводе всех групп
@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('back_btn'))
async def ik_cb_back_btn_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Выберите опцию:",
                                     reply_markup=get_unline_keyboard('3'))

#---Функция для получения всех действующих групп для рассылки
async def get_all_reply_groups():
    result = "Группы для рассылки:\n"
    for group in group_host:
        try:
            result += group.title + "\n"
        except Exception:
            continue
    return result

#---Функция для добавления группы в рассылку
async def add_group_to_reply(group_chat):
    if group_chat not in group_host:
        group_host.append(group_chat)

#---Функция для рассылки сообщений во все группы
async def send_messages_to_groups(message_to_send):
    str_result = ""
    for group in group_host:
        try:
            await bot.send_message(chat_id=group.id,
                               text=message_to_send)
            str_result+=f"Сообщение в группу {group.title} успешно отправлено\n"
        except Exception:
            print(Exception)
            str_result+="С одной из групп произошла проблема! \n"
            continue
    return str_result


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)

