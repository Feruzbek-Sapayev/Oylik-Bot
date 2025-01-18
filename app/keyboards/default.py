from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup( resize_keyboard=True, keyboard=[
    [KeyboardButton(text="🧾 Иш ҳақи тўғрисида маълумот олиш")], 
    [KeyboardButton(text='⚙️ Созламалар')]
])

main_markup_for_admin = ReplyKeyboardMarkup( resize_keyboard=True, keyboard=[
    [KeyboardButton(text="📤 Файл юклаш"), KeyboardButton(text="🗑 Файл ўчириш")], 
    [KeyboardButton(text="🧾 Иш ҳақи тўғрисида маълумот олиш"), KeyboardButton(text='⚙️ Созламалар')]
])

settings_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text="☎️ Телефон рақамни ўзгартириш"), KeyboardButton(text="🔏 ЖШШИР ни ўзгартириш")],
    [KeyboardButton(text='⬅️ Орқага')]
])

share_contact_btn = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text="📞 Телефон ракамни юбориш", request_contact=True)]
])

back_btn = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='⬅️ Орқага')]
])
