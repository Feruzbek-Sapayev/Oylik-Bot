from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import FSInputFile
from aiogram import F, Router
from aiogram.enums import ParseMode, ChatAction
import asyncio
from aiogram.fsm.context import FSMContext
from app.states.state import RegisterState, UserState, SettingsState, AdminState
from app.keyboards.default import main_markup, share_contact_btn, settings_markup, back_btn, main_markup_for_admin
from app.keyboards.inline import get_month_markup
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from app.database import db
from environs import Env
from aiogram import Bot
import os
from excel import get_excel

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

ADMINS = env.list("ADMINS")
BOT_TOKEN = env.str("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

user = Router()


def get_month_names():
    folder_path = 'D:\\Telegram bot\\oylik_bot\\app\\files'
    excel_files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.xls'))]
    excel_files_names = []
    for i in excel_files:
        name, s = i.split('.')
        excel_files_names.append(name)
    return excel_files_names

def get_excel_paths():
    folder_path = 'D:\\Telegram bot\\oylik_bot\\app\\files'
    excel_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.xls'))]
    return excel_files

@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await db.select_user(message.from_user.id)
    if user:
        if str(message.from_user.id) in ADMINS:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup_for_admin, parse_mode='html')
            await state.set_state(UserState.main)
        else:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup, parse_mode='html')
            await state.set_state(UserState.main)
    else:
        await message.answer("<b>Телефон рақамингизни киритиш учун 👇 тугмани босинг</b>", reply_markup=share_contact_btn, parse_mode='html')
        await state.set_state(RegisterState.phone_number)

@user.message(RegisterState.phone_number)
async def get_phone_number(message: Message, state: FSMContext):
    if message.contact:
        await message.answer("<b>📤 ЖШШИР ни киритинг</b>\n\n<i>ЖШШИР 14 та рақамдан иборат бўлади</i>", reply_markup=ReplyKeyboardRemove(), parse_mode='html')
        await state.set_data({'phone_number': message.contact.phone_number})
        await state.set_state(RegisterState.jshshir)
    else:
        await message.answer("<b>❗️ Телефон ракамини факатгина пастдаги тугмани босинг оргали юборинг👇</b>", reply_markup=share_contact_btn, parse_mode='html')

@user.message(RegisterState.jshshir)
async def get_jshshir(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and len(message.text) == 14:
        if str(message.from_user.id) in ADMINS:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup_for_admin, parse_mode='html')
        else:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup, parse_mode='html')
        phone_number = (await state.get_data())['phone_number']
        await db.add_user(message.from_user.id, phone_number, message.text)
        await state.set_state(UserState.main)
    else:
        await message.answer("<b>📤 ЖШШИР ни киритинг</b>\n\n<i>ЖШШИР 14 та рақамдан иборат бўлади</i>", reply_markup=ReplyKeyboardRemove(), parse_mode='html')


@user.message(UserState.main)
async def main_state_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == "⚙️ Созламалар":
            await message.answer("<b>Ўзгартирмоқчи бўлган маълумотингизни танланг 👇</b>", reply_markup=settings_markup, parse_mode="html")
            await state.set_state(UserState.settings)
        
        if message.text == "📤 Файл юклаш" and str(message.from_user.id) in ADMINS:
            await message.answer("<b>Ойлик хакида малумотни ехсель шаклида юборинг:</b>\n\n Масалан: 2024-11.xlsx", reply_markup=back_btn, parse_mode="html")
            await state.set_state(AdminState.upload_file)

        if message.text == "🧾 Иш ҳақи тўғрисида маълумот олиш":
            markup = get_month_markup(get_month_names(), 'r')
            await message.answer("<b>Кўрмоқчи бўлган даврингизни киритинг! 📝\nМисол учун: 2021-09</b>", parse_mode='html', reply_markup=back_btn)
            await message.answer("<b>Ёки қуйидагилардан бирини танланг 👇</b>", parse_mode='html', reply_markup=markup)
            await state.set_state(UserState.get_month)
        
        if message.text == "🗑 Файл ўчириш" and str(message.from_user.id) in ADMINS:
            files = get_month_names()
            txt = '<b>Мавжуд файллар:</b>\n\n'
            for file in files:
                txt += f"<code>{file}</code>,   "
            txt += "\n\n<b>Ўчирмокчи бўлган файлнинг номини ёзинг</b>"
            await message.answer(txt, parse_mode='html', reply_markup=back_btn)
            await state.set_state(AdminState.delete_file)
    else:
        if str(message.from_user.id) in ADMINS:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup_for_admin, parse_mode='html')
        else:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup, parse_mode='html')


@user.message(AdminState.upload_file)
async def admin_state_handler(message: Message, state: FSMContext):
    if message.document:
        file_name, file_type = message.document.file_name.split('.')
        file_id = message.document.file_id
        if file_type in ['xls', 'xlsx']:
            file = await bot.get_file(file_id)
            file_path = file.file_path
            destination = os.path.join("app/files", message.document.file_name)
            await bot.download_file(file_path, destination)
            await message.answer(f"<b>{message.document.file_name} сакланди✅</b>", parse_mode='html')
            
        else:
            await message.answer("<b>Ойлик хакида малумотни ехсель шаклида юборинг:</b>\n\nMasalan: 2024-11.xlsx", reply_markup=back_btn, parse_mode="html")
    elif message.text:
        if message.text == "⬅️ Орқага":
            if str(message.from_user.id) in ADMINS:
                await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup_for_admin, parse_mode='html')
                await state.set_state(UserState.main)
            else:
                await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup, parse_mode='html')
                await state.set_state(UserState.main)
    else:
        await message.answer("<b>Ойлик хакида малумотни ехсель шаклида юборинг:</b>\n\n Масалан: 2024-11.xlsx", reply_markup=back_btn, parse_mode="html")


@user.message(AdminState.delete_file)
async def admin_state_handler2(message: Message, state: FSMContext):
    files = get_month_names()
    if message.text and message.text in files:
        file_paths = get_excel_paths()
        file_path = None
        for path in file_paths:
            if message.text in path:
                file_path = path
                break
        if file_path:
            try:
                os.remove(path)
                await message.answer("<b>✅ Файл ўчирилди 🗑</b>", parse_mode='html')
                files = get_month_names()
                txt = '<b>Мавжуд файллар:</b>\n\n'
                for file in files:
                    txt += f"<code>{file}</code>,   "
                txt += "\n\n<b>Ўчирмокчи бўлган файлнинг номини ёзинг</b>"
                await message.answer(txt, parse_mode='html', reply_markup=back_btn)
            except:
                await message.answer(f"<b>{message.text} номли файлни ўчириб бўлмади🙁<b>", parse_mode='html', reply_markup=back_btn)
        else:
            await message.answer(f"<b>{message.text} номли файл топилмади🙁</b>", parse_mode='html', reply_markup=back_btn)
    elif message.text and message.text == "⬅️ Орқага":
        if str(message.from_user.id) in ADMINS:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup_for_admin, parse_mode='html')
        else:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup, parse_mode='html')
        await state.set_state(UserState.main)
    
    else:
        files = get_month_names()
        txt = '<b>Мавжуд файллар:</b>\n\n'
        for file in files:
            txt += f"<code>{file}</code>,   "
        txt += "\n\n<b>Ўчирмокчи бўлган файлнинг номини ёзинг</b>"
        await message.answer(txt, parse_mode='html', reply_markup=back_btn)

@user.message(UserState.settings)
async def settings_state_handler(message: Message, state: FSMContext):
    if message.text and message.text == "☎️ Телефон рақамни ўзгартириш":
        await message.answer("<b>Телефон рақамингизни киритиш учун 👇 тугмани босинг</b>", reply_markup=share_contact_btn, parse_mode='html')
        await state.set_state(SettingsState.phone_number)
    elif message.text and message.text == "🔏 ЖШШИР ни ўзгартириш":
        await message.answer("<b>📤 ЖШШИР ни киритинг</b>\n\n<i>ЖШШИР 14 та рақамдан иборат бўлади</i>", reply_markup=back_btn, parse_mode='html')
        await state.set_state(SettingsState.jshshir)
    elif message.text == "⬅️ Орқага":
        if str(message.from_user.id) in ADMINS:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup_for_admin, parse_mode='html')
        else:
            await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup, parse_mode='html')
        await state.set_state(UserState.main)
    else:
        await message.answer("<b>Ўзгартирмоқчи бўлган маълумотингизни танланг 👇</b>", reply_markup=settings_markup, parse_mode="html")




@user.message(SettingsState.phone_number)
async def edit_phone_number(message: Message, state: FSMContext):
    if message.contact:
        await db.update_user_phone(message.from_user.id, message.contact.phone_number)
        if str(message.from_user.id) in ADMINS:
            await message.answer("<b>☎️ Телефон рақамингиз ўзгартирилди ✅</b>", reply_markup=main_markup_for_admin, parse_mode='html')
        else:
            await message.answer("<b>☎️ Телефон рақамингиз ўзгартирилди ✅</b>", reply_markup=main_markup, parse_mode='html')
        await state.set_state(UserState.main)
    else:
        await message.answer("<b>❗️ Телефон ракамини факатгина пастдаги тугмани босинг оргали юборинг👇</b>", reply_markup=share_contact_btn, parse_mode='html')


@user.message(SettingsState.jshshir)
async def edit_jshshir(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and len(message.text) == 14:
        await db.update_user_jshshir(message.from_user.id, message.text)
        if str(message.from_user.id) in ADMINS:
            await message.answer("<b>📤 ЖШШИР ўзгартирилди✅</b>", reply_markup=main_markup_for_admin, parse_mode='html')
        else:
            await message.answer("<b>📤 ЖШШИР ўзгартирилди✅</b>", reply_markup=main_markup, parse_mode='html')
        await state.set_state(UserState.main)
    elif message.text and message.text == "⬅️ Орқага":
        await message.answer("<b>Ўзгартирмоқчи бўлган маълумотингизни танланг 👇</b>", reply_markup=settings_markup, parse_mode="html")
        await state.set_state(UserState.settings)
    else:
        await message.answer("<b>📤 ЖШШИР ни киритинг</b>\n\n<i>ЖШШИР 14 та рақамдан иборат бўлади</i>", reply_markup=back_btn, parse_mode='html')


@user.message(UserState.get_month)
async def get_month_handler(message: Message, state: FSMContext):
    if message.text:
        months = get_month_names()
        if message.text in months:
            user = await db.select_user(message.from_user.id)
            call_data = message.text
            yil, oy = call_data.split('-')
            paths = get_excel_paths()
            excel_path = ''
            for path in paths:
                if call_data in path:
                    excel_path = path
                    break
            data = get_excel(excel_path)
            oylar = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
            user_data = None
            for i in data:
                if i[1]!="nan" and i[1]!=" ":
                    i[1] = int(float(i[1]))
                else:
                    i[1] = 0

                if i[4]!="nan" and i[4]!=" ":
                    i[4] = int(float(i[4]))
                else:
                    i[4] = 0

                if i[5]!='nan' and i[5]!=" ":
                    i[5] = float(i[5])
                else:
                    i[5] = 0

                if i[6]!="nan" and i[6]!=' ':
                    i[6] = int(float(i[6]))
                else:
                    i[6] = 0

                if i[7]!="nan" and i[7]!=' ':
                    i[7] = float(i[7])
                else:
                    i[7] = 0

                if i[8]!="nan" and i[8]!=' ':
                    i[8] = float(i[8])
                else:
                    i[8] = 0

                if i[9]!="nan" and i[9]!=' ':
                    i[9] = int(float(i[9]))
                else:
                    i[9] = 0

                if i[10]!="nan" and i[10]!=' ':
                    i[10] = int(float(i[10]))
                else:
                    i[10] = 0

                if i[11]!="nan" and i[11]!=' ':
                    i[11] = int(float(i[11]))
                else:
                    i[11] = 0

                if i[12]!="nan" and i[12]!=' ':
                    i[12] = int(float(i[12]))
                else:
                    i[12] = 0

                if i[13]!="nan" and i[13]!=' ':
                    i[13] = int(float(i[13]))
                else:
                    i[13] = 0
                if int(user.jshshir) == i[1]:
                    user_data = i
                    text = (
                        f"Исми ва фамилияси: <b>{i[2]}</b>\n"
                        f"Лавозими: <b>{i[3]}</b>\n\n"
                        f"<b>{yil} йил {oylar[int(oy)-1]} ойи учун:</b>\n"
                        f"- Лавозим оклади: <b>{f'{i[4]:,}'.replace(',', ' ')}</b> сўм\n"
                        f"- Подъемный балл: <b>{i[5]} балл</b>\n"
                        f"- Подьемный оклад: <b>{f'{i[6]:,}'.replace(',', ' ')} сўм</b>\n"
                        f"- Ишланган соат: <b>{i[7]} соат</b>\n"
                        f"- Выслуга лет стажи: <b>{i[8]}  йил ( {i[9]}% окладдан фоиз)</b>\n"
                        f"- Выслуга лет устамаси: <b>{f'{i[10]:,}'.replace(',', ' ')} сўм</b>\n"
                        f"- Жами ҳисобланган иш ҳақи: <b>{f'{i[11]:,}'.replace(',', ' ')} сўм</b>\n"
                    )
                    if int(i[12]) != 0:
                        text += (
                            f"- Жарималар: <b>{f'{i[12]:,}'.replace(',', ' ')} сўм</b>\n"
                        )
                    if int(i[13]) != 0:
                        text += (
                            f"- Корхонага кредит тўлови: <b>{f'{i[13]:,}'.replace(',', ' ')} сўм</b>"
                        )
                    await message.answer(text, parse_mode='html', reply_markup=back_btn)
                    break
            if user_data is None:
                await message.answer("<b>Кўрсатылган ЖШШИР га оид хеч кандай маьлумот топилмади🙁\n\nHR га мурожаат килинг!</b>", parse_mode='html')
        
        elif message.text == '⬅️ Орқага':
            if str(message.from_user.id) in ADMINS:
                await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup_for_admin, parse_mode='html')
            else:
                await message.answer("<b>Ойлик ҳақида маълумот олиш учун қуйидаги тугмалардан бирини танланг 👇</b>", reply_markup=main_markup, parse_mode='html')
            await state.set_state(UserState.main)

        
        
        
        
        else:
            await message.answer("<b>Кўрсатилган даврга оид маьлумотлар топилмади🙁</b>", parse_mode='html')
    else:
        await message.answer("<b>Кўрмоқчи бўлган даврингизни киритинг! 📝\nМисол учун: 2021-09</b>", parse_mode='html', reply_markup=back_btn)


@user.callback_query()
async def pick_month_state_call(call: CallbackQuery, state: FSMContext):
    months = get_month_names()
    user = await db.select_user(call.from_user.id)
    if call.data.startswith('r'):
        key, call_data = call.data.split('_')
        yil, oy = call_data.split('-')
        paths = get_excel_paths()
        excel_path = ''
        for path in paths:
            if call_data in path:
                excel_path = path
                break
        data = get_excel(excel_path)
        oylar = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        user_data = None
        for i in data:
            if i[1]!="nan" and i[1]!=" ":
                i[1] = int(float(i[1]))
            else:
                i[1] = 0

            if i[4]!="nan" and i[4]!=" ":
                i[4] = int(float(i[4]))
            else:
                i[4] = 0

            if i[5]!='nan' and i[5]!=" ":
                i[5] = float(i[5])
            else:
                i[5] = 0

            if i[6]!="nan" and i[6]!=' ':
                i[6] = int(float(i[6]))
            else:
                i[6] = 0

            if i[7]!="nan" and i[7]!=' ':
                i[7] = float(i[7])
            else:
                i[7] = 0

            if i[8]!="nan" and i[8]!=' ':
                i[8] = float(i[8])
            else:
                i[8] = 0

            if i[9]!="nan" and i[9]!=' ':
                i[9] = int(float(i[9]))
            else:
                i[9] = 0

            if i[10]!="nan" and i[10]!=' ':
                i[10] = int(float(i[10]))
            else:
                i[10] = 0

            if i[11]!="nan" and i[11]!=' ':
                i[11] = int(float(i[11]))
            else:
                i[11] = 0

            if i[12]!="nan" and i[12]!=' ':
                i[12] = int(float(i[12]))
            else:
                i[12] = 0

            if i[13]!="nan" and i[13]!=' ':
                i[13] = int(float(i[13]))
            else:
                i[13] = 0
            if int(user.jshshir) == i[1]:
                user_data = i
                text = (
                    f"Исми ва фамилияси: <b>{i[2]}</b>\n"
                    f"Лавозими: <b>{i[3]}</b>\n\n"
                    f"<b>{yil} йил {oylar[int(oy)-1]} ойи учун:</b>\n"
                    f"- Лавозим оклади: <b>{f'{i[4]:,}'.replace(',', ' ')}</b> сўм\n"
                    f"- Подъемный балл: <b>{i[5]} балл</b>\n"
                    f"- Подьемный оклад: <b>{f'{i[6]:,}'.replace(',', ' ')} сўм</b>\n"
                    f"- Ишланган соат: <b>{i[7]} соат</b>\n"
                    f"- Выслуга лет стажи: <b>{i[8]}  йил ( {i[9]}% окладдан фоиз)</b>\n"
                    f"- Выслуга лет устамаси: <b>{f'{i[10]:,}'.replace(',', ' ')} сўм</b>\n"
                    f"- Жами ҳисобланган иш ҳақи: <b>{f'{i[11]:,}'.replace(',', ' ')} сўм</b>\n"
                )
                if int(i[12]) != 0:
                    text += (
                        f"- Жарималар: <b>{f'{i[12]:,}'.replace(',', ' ')} сўм</b>\n"
                    )
                if int(i[13]) != 0:
                    text += (
                        f"- Корхонага кредит тўлови: <b>{f'{i[13]:,}'.replace(',', ' ')} сўм</b>"
                    )
                await call.message.answer(text, parse_mode='html', reply_markup=back_btn)
                break
        if user_data is None:
            await call.message.answer("<b>Кўрсатылган ЖШШИР га оид хеч кандай маьлумот топилмади🙁\n\nHR га мурожаат килинг!</b>", parse_mode='html')
    await call.answer()



@user.message()
async def no_state_handler(message: Message):
    await message.answer("Ботни ишга тушириш👇\n\n/start /start /start")