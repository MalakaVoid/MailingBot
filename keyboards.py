from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery


def get_inline_keyboard(id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    if id == 'main_menu_ikb':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать рассылку",
                                  callback_data='start_mailing_mm_btn')],
            [InlineKeyboardButton(text="Группы для рассылки",
                                  callback_data='mailings_groups_mm_btn')],
            [InlineKeyboardButton(text="Удалить группу из рассылки",
                                  callback_data='del_mailing_group_mm_btn')]
        ])
    elif id == 'cancel_mailing_ikb':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отмена",
                                  callback_data='cancel_mailing_c_btn')]
        ])
    elif id == 'check_correctness_msg_ikb':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отправить",
                                  callback_data='send_mail_msg_btn')],
            [InlineKeyboardButton(text="Изменить",
                                  callback_data='edit_msg_btn')]
        ])
    return ikb