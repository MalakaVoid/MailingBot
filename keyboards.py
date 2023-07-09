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
                                  callback_data='del_mailing_group_mm_btn')],
            [InlineKeyboardButton(text="Панель администратора",
                                  callback_data='admins_panel_mm_btn')]
        ])
    elif id == 'admins_panel_adm_ikb':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Добавить админа",
                                  callback_data='add_admin_adm_btn'),
             InlineKeyboardButton(text="Удалить админа",
                                  callback_data='del_admin_adm_btn')],
            [InlineKeyboardButton(text="Админы",
                                  callback_data='get_admins_adm_btn')],
            [InlineKeyboardButton(text="Назад",
                                  callback_data='back_sh_btn')]
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
    elif id == 'back_mm_sh_ikb':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад",
                                  callback_data='back_sh_btn')]
        ])
    return ikb