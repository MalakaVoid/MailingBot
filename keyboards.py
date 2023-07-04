from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery


def get_unline_keyboard(id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    if id == '1':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('Да',
                                  callback_data='add_group_to_reply_start_btn'),
             InlineKeyboardButton('Нет',
                                  callback_data='no_add_group_to_reply_start_btn')
             ]
        ])
    elif id == '2':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('Да',
                                  callback_data='yes_del_btn'),
             InlineKeyboardButton('Нет',
                                  callback_data='no_del_btn')
             ]
        ])
    elif id == '3':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('Начать рассылку',
                                  callback_data='start_reply_btn')],
             [InlineKeyboardButton('Показать группы для рассылки',
                                  callback_data='show_groups_reply_btn')
             ]
        ])
    elif id == '4':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('Отмена',
                                  callback_data='cancel_btn')
        ]])
    elif id == '5':
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('Назад',
                                  callback_data='back_btn')
        ]])

    return ikb