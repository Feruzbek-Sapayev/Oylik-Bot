from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Orqaga', callback_data='back')]
])


def get_month_markup(excel_files_names, key):
    if len(excel_files_names) > 12:
        excel_files_names = excel_files_names[:12]
    builder = InlineKeyboardBuilder()
    for i in excel_files_names:
        builder.add(InlineKeyboardButton(text=i, callback_data=f"{key}_{i}"))
    builder.adjust(4)
    return builder.as_markup()