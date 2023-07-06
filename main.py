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


@dp.message_handler()
async def get_message_of_group(message: types.Message):
    if message.chat.type == "group":
        print(message.chat)
        if message.chat not in group_host:
            group_host.append(message.chat)
            print(group_host)




if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)

