from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from db_controller import delete_group_from_database, delete_admin_from_database, add_group_to_database,add_admin_to_database, is_admin_here, get_chat_ids, parse_group_chat_ids_into_arr, parse_group_chat_titles_into_arr, chat_id_by_title_group, catch_admins_from_database
from globals import TOKEN_API, group_title,group_chat_id
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
group_chat_id = parse_group_chat_ids_into_arr()
group_title = parse_group_chat_titles_into_arr()
#---Класс состояний, enterMessage - для ожидания сообщений для рассылки
class ReplyST(StatesGroup):
    enterMessage = State()

class DeleteGroupST(StatesGroup):
    enterGroupName = State()

class AdminMngm(StatesGroup):
    addAdmin = State()
    delAdmin = State()

@dp.message_handler(commands=['start'])
async def start_btn_hndl(message: types.Message):
    if message.chat.type == "private":
        if is_admin_here(message.chat.username):
            await send_main_menu_mes(message.chat.id)

@dp.message_handler(state=AdminMngm.addAdmin)
async def add_admin_to_db_hndl(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if is_admin_here(message.chat.username):
            add_admin_to_database(message.text)
            await state.finish()
            await bot.send_message(message.chat.id,
                                   text="Новый админ успешно добавлен",
                                   reply_markup=get_inline_keyboard('back_mm_sh_ikb'))

@dp.message_handler(state=AdminMngm.delAdmin)
async def del_admin_to_db_hndl(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if is_admin_here(message.chat.username):
            if is_admin_here(message.text):
                delete_admin_from_database(message.text)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       text="Админ успешно удален",
                                       reply_markup=get_inline_keyboard('back_mm_sh_ikb'))
            else:
                await bot.send_message(message.chat.id,
                                       text="Такого админа не существует. Попробуйте еще раз.",
                                       reply_markup=get_inline_keyboard('cancel_mailing_ikb'))

@dp.message_handler(state=ReplyST.enterMessage)
async def get_message_to_mail(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if is_admin_here(message.chat.username):
            await state.finish()
            await bot.send_message(message.chat.id,
                                   text=message.text,
                                   reply_markup=get_inline_keyboard('check_correctness_msg_ikb'))

@dp.message_handler(state=DeleteGroupST.enterGroupName)
async def get_message_group_title_to_delete(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if is_admin_here(message.chat.username):
            if message.text not in group_title:
                await bot.send_message(message.chat.id,
                                       text="Данная группа не найдена, попробуйте еще раз",
                                       reply_markup=get_inline_keyboard('cancel_mailing_ikb'))
            else:
                await state.finish()
                id_chat_to_del = chat_id_by_title_group(message.text)
                await bot.leave_chat(chat_id=id_chat_to_del)
                delete_group_from_database(message.text)
                group_title.remove(message.text)
                group_chat_id.remove(id_chat_to_del)
                await bot.send_message(message.chat.id,
                                       text="Группа успешно удалена!",
                                       reply_markup=get_inline_keyboard('back_mm_sh_ikb'))

@dp.message_handler(state=None)
async def get_message_of_group(message: types.Message):
    if message.chat.type == "group":
        if message.chat.title not in group_title and message.chat.id not in group_chat_id:
            await add_group_to_db(message.chat)

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('mm_btn'))
async def main_menu_ikb_hndl(callback: types.CallbackQuery):
    if callback.data == 'start_mailing_mm_btn':
        await ReplyST.enterMessage.set()
        await callback.message.edit_text(text='Введите сообщение для рассылки',
                                         reply_markup=get_inline_keyboard('cancel_mailing_ikb'))
    elif callback.data == 'mailings_groups_mm_btn':
        str_groups = ""
        for each in group_title:
            str_groups += each + "\n"
        await callback.message.edit_text(text=str_groups,
                                         reply_markup=get_inline_keyboard('back_mm_sh_ikb'))
    elif callback.data == 'del_mailing_group_mm_btn':
        await DeleteGroupST.enterGroupName.set()
        await callback.message.edit_text(text="Введите название группы для удаления",
                                         reply_markup=get_inline_keyboard('cancel_mailing_ikb'))
    elif callback.data == 'admins_panel_mm_btn':
        await callback.message.edit_text(text="Выберите опцию",
                                         reply_markup=get_inline_keyboard('admins_panel_adm_ikb'))

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('adm_btn'))
async def admins_panel_mngm(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'add_admin_mm_btn':
        await AdminMngm.addAdmin.set()
        await callback.message.edit_text(text="Введите ник админа",
                                         reply_markup=get_inline_keyboard('cancel_mailing_ikb'))
    elif callback.data == 'del_admin_mm_btn':
        await AdminMngm.delAdmin.set()
        await callback.message.edit_text(text="Введите ник админа",
                                         reply_markup=get_inline_keyboard('cancel_mailing_ikb'))
    elif callback.data == 'get_admins_mm_btn':
        arr_admins = catch_admins_from_database()
        str_admins = ""
        for each in arr_admins:
            str_admins += each + "\n"
        await callback.message.edit_text(text=str_admins,
                                         reply_markup=get_inline_keyboard('back_mm_sh_ikb'))

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('c_btn'), state=[ReplyST.enterMessage, DeleteGroupST.enterGroupName, AdminMngm.delAdmin, AdminMngm.addAdmin])
async def cancel_mailing_btn(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await send_main_menu_mes(callback.message.chat.id)
    await callback.message.delete_reply_markup()

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('c_btn'), state=None)
async def cancel_mailing_err_btn(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('msg_btn'))
async def check_correctness_ikb_hndl(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'send_mail_msg_btn':
        await send_messages_to_groups(callback.message.text)
        await callback.message.edit_text(text="Выберите опцию",
                                         reply_markup=get_inline_keyboard('main_menu_ikb'))
    elif callback.data == 'edit_msg_btn':
        await ReplyST.enterMessage.set()
        await callback.message.edit_text(text='Введите сообщение для рассылки',
                                         reply_markup=get_inline_keyboard('cancel_mailing_ikb'))

@dp.callback_query_handler(lambda callback_querry: callback_querry.data.endswith('sh_btn'))
async def back_to_menu_btn_hndl(callback: types.CallbackQuery):
    if callback.data == 'back_sh_btn':
        await callback.message.edit_text(text="Выберите опцию",
                                         reply_markup=get_inline_keyboard('main_menu_ikb'))

async def send_main_menu_mes(chat_id):
    await bot.send_message(chat_id=chat_id,
                           text="Выберите опцию:",
                           reply_markup=get_inline_keyboard('main_menu_ikb'))

async def add_group_to_db(chat_ex):
    group_title.append(str(chat_ex.title))
    group_chat_id.append(str(chat_ex.id))
    add_group_to_database(chat_ex.id, chat_ex.title, chat_ex.type)

async def send_messages_to_groups(msg_text):
    for each in group_chat_id:
        await bot.send_message(chat_id=each,
                               text=msg_text)



if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)

