from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.main_inline import *
from keyboards.inline.menu_button import *
from loader import dp, bot
from utils.db_api.database import *
import datetime
from aiogram.types import ReplyKeyboardRemove
from geopy.geocoders import Nominatim
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultPhoto, InputMediaPhoto, InlineQueryResultArticle
from aiogram.utils.deep_linking import decode_payload, get_start_link
import re
import random
import requests


def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)


def generateOTP():
    return random.randint(111111, 999999)


def send_sms(otp, phone):
    username = "idealdent"
    password = "(k5BS#7&Duu2"
    sms_data = {
        "messages":[{"recipient":f"{phone}","message-id":"abc000000003","sms":{"originator": "3700","content": {"text": f"Sizning Ideal Dent botida ro'yxatdan o'tish kodingiz: {otp}"}}}]}
    url = "http://91.204.239.44/broker-api/send"
    res = requests.post(url=url, headers={}, auth=(username, password), json=sms_data)


@dp.message_handler(lambda message: message.text in ["🏠 Asosiy menyu", "🏠 Main menu", "🏠 Главное меню"], state='*')
async def go_home(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    markup = await user_menu(lang)
    if lang == "uz":
        await message.answer("Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
    elif lang == "ru":
        await message.answer("Добро пожаловать в наш бот. Выберите нужный раздел👇", reply_markup=markup)
    elif lang == "en":
        await message.answer("Welcome to our bot. Please select the desired section 👇", reply_markup=markup)
    await state.set_state("get_command")
 

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    user = await get_user(message.from_id)
    if user is not None:
        if user.lang:
            lang = await get_lang(message.from_user.id)
            if user.name:
                markup = await user_menu(lang)
                if lang == "uz":
                    await message.answer("Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
                elif lang == "ru":
                    await message.answer("Добро пожаловать в наш бот. Выберите нужный раздел👇", reply_markup=markup)
                elif lang == "en":
                    await message.answer("Welcome to our bot. Please select the desired section 👇", reply_markup=markup)
                await state.set_state("get_command")
            else:
                markup = await back_keyboard(lang)
                if lang == "uz":
                    await message.answer("Iltimos ismingizni kiriting 👇", reply_markup=markup)
                elif lang == "ru":
                    await message.answer("Пожалуйста, введите ваше имя 👇", reply_markup=markup)
                elif lang == "en":
                    await message.answer("Please enter your name 👇", reply_markup=markup)
                await state.set_state("get_name")   
        else:
            markup =await language_keyboard()
            await message.answer(f"Assalomu alaykum, {message.from_user.first_name}👋. \nKerakli tilni tanlang 👇\n\nHello, {message.from_user.first_name}👋. \nChoose the language you need 👇\n\nЗдравствуйте, {message.from_user.first_name}👋. \nВыберите нужный язык 👇", 
                                reply_markup=markup)
            await state.set_state("get_lang")     
    else:
        args = message.get_args()
        payload = decode_payload(args)
        if payload != '':
            await add_user(user_id=message.from_user.id, referal_user=payload)
        else:
            await add_user(user_id=message.from_user.id, referal_user="no_referal")
        markup =await language_keyboard()
        await message.answer(f"Assalomu alaykum, {message.from_user.first_name}👋. \nKerakli tilni tanlang 👇\n\nHello, {message.from_user.first_name}👋. \nChoose the language you need 👇\n\nЗдравствуйте, {message.from_user.first_name}👋. \nВыберите нужный язык 👇", 
                            reply_markup=markup)
        await state.set_state("get_lang")


@dp.message_handler(state="get_lang")
async def get_language(message: types.Message, state: FSMContext):
    if message.text in ["🇺🇿 O'zbek tili", "🇺🇸 English", "🇷🇺 Русский язык"]:
        if message.text == "🇺🇿 O'zbek tili":
            data = "uz"
        elif message.text == "🇺🇸 English":
            data = "en"
        elif message.text == "🇷🇺 Русский язык":
            data = "ru"
        user = await get_user(message.from_user.id)
        user.lang = data
        user.save()
        lang = await get_lang(message.from_user.id)
        markup = await back_keyboard(lang)
        if lang == "uz":
            await message.answer("Iltimos ismingizni kiriting 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Пожалуйста, введите ваше имя 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Please enter your name 👇", reply_markup=markup)
        await state.set_state("get_name")
    else:
        markup =await language_keyboard()
        await message.answer(f"Kerakli tilni tanlang 👇\nChoose the language you need 👇\nВыберите нужный язык 👇", 
                            reply_markup=markup)
        await state.set_state("get_lang")


@dp.message_handler(state="get_name", content_types=types.ContentTypes.TEXT)
async def get_name(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)            
    if message.text in ["⬅️ Orqaga", "⬅️ Back", "⬅️ Назад"]:
        markup =await language_keyboard()
        await message.answer(f"Kerakli tilni tanlang 👇\nChoose the language you need 👇\nВыберите нужный язык 👇", 
                            reply_markup=markup)
        await state.set_state("get_lang")
    else:         
        user = await get_user(message.from_user.id)
        user.name = message.text
        user.save()
        markup = await phone_keyboard(lang)
        if lang == "uz":
            await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Enter your phone number in international format (<b>998YYXXXXXX</b>). Or share the number 👇", reply_markup=markup)
        await state.set_state("get_phone_number")


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state="get_phone_number")
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number[1:]
        user = await get_user(message.from_user.id)
        user.new_phone = phone
        otp = generateOTP()
        send_sms(otp=otp, phone=phone)
        user.otp = otp
        user.save()
        print(user.otp)
        lang = await get_lang(message.from_user.id)
        keyboard = await back_keyboard(lang)
        if lang == "uz":
            await message.answer(text=f"<b>{user.new_phone}</b> raqamiga yuborilgan tasdiqlash kodini kiriting", parse_mode='HTML', reply_markup=keyboard)
        if lang == "ru":
            await message.answer(text=f"Введите код подтверждения, отправленный на номер <b>{user.new_phone}</b>.", parse_mode='HTML', reply_markup=keyboard)
        if lang == "en":
            await message.answer(text=f"Enter the verification code sent to <b>{user.new_phone}</b>", parse_mode='HTML', reply_markup=keyboard)
        await state.set_state("get_otp")
    

@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_phone_number")
async def get_phone(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if "⬅️️" in message.text:
        user = await get_user(message.from_id)
        if user is not None:
            lang = await get_lang(message.from_user.id)
            if user.phone is not None:
                markup = await user_menu(lang)
                if lang == "uz":
                    await message.answer("Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
                elif lang == "en":
                    await message.answer("Welcome to our bot. Choose the section you want 👇", reply_markup=markup)
                elif lang == "ru":
                    await message.answer("Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
                await state.set_state("get_command")
            else:
                markup = await phone_keyboard(lang)
                if lang == "uz":
                    await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
                elif lang == "en":
                    await message.answer("Enter your phone number in international format (<b>998YYXXXXXX</b>). Or share the number 👇", reply_markup=markup)
                elif lang == "ru":
                    await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
                await state.set_state("get_phone_number")            
        else:
            markup =await language_keyboard()
            await message.answer(f"Assalomu alaykum, {message.from_user.first_name}👋. \nKerakli tilni tanlang 👇\n\nHello, {message.from_user.first_name}👋. \nChoose the language you need 👇\n\nЗдравствуйте, {message.from_user.first_name}👋. \nВыберите нужный язык 👇", 
                                reply_markup=markup)
            await state.set_state("get_lang")
    else:
        if isValid(message.text):
            phone = message.text
            user = await get_user(message.from_user.id)
            user.new_phone = phone
            otp = generateOTP()
            send_sms(otp=otp, phone=phone)
            user.otp = otp
            user.save()
            print(user.otp)
            keyboard = await back_keyboard(lang)
            if lang == "uz":
                await message.answer(text=f"<b>{user.new_phone}</b> raqamiga yuborilgan tasdiqlash kodini kiriting", parse_mode='HTML', reply_markup=keyboard)
            if lang == "en":
                await message.answer(text=f"Введите код подтверждения, отправленный на номер <b>{user.new_phone}</b>.", parse_mode='HTML', reply_markup=keyboard)
            if lang == "ru":
                await message.answer(text=f"Enter the verification code sent to <b>{user.new_phone}</b>", parse_mode='HTML', reply_markup=keyboard)
            await state.set_state("get_otp")
        else:
            markup = await phone_keyboard(lang)
            if lang == "uz":
                await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
            elif lang == "en":
                await message.answer("Enter your phone number in international format (<b>998YYXXXXXX</b>). Or share the number 👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
            await state.set_state("get_phone_number")            
        

@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_otp")
async def get_phone(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user.lang
    if "⬅️️" in message.text: 
        markup = await phone_keyboard(lang)
        if lang == "uz":
            await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Enter your phone number in international format (<b>998YYXXXXXX</b>). Or share the number 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
        await state.set_state("get_phone_number")            
    else:
        if message.text == user.otp:
            user.phone = user.new_phone
            user.save()
            markup = await user_menu(lang)
            if lang == "uz":
                await message.answer("Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
            elif lang == "en":
                await message.answer("Welcome to our bot. Choose the section you want 👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
            await state.set_state("get_command")
        else:
            lang = await get_lang(message.from_user.id)
            markup = await back_keyboard(lang)
            if lang == "uz":
                await message.answer("⚠️ Yuborilgan tasdiqlash kodi xato. Qayta urinib ko'ring", reply_markup=markup)
            elif lang == "en":
                await message.answer("⚠️ The verification code sent is incorrect. Try again", reply_markup=markup)
            elif lang == "ru":
                await message.answer("⚠️ Присланный проверочный код неверный. Попробуйте еще раз", reply_markup=markup)
            await state.set_state("get_otp")


@dp.message_handler(state="get_command", content_types=types.ContentTypes.TEXT)
async def get_user_command(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    command = message.text
    if command in ["⚙️ Sozlamalar", "⚙️ Настройки", "⚙️ Settings"]:
        markup = await settings_keyboard(lang)
        if lang == "uz":
            await message.answer(text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer(text="Choose the command you want 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer(text="Выберите нужную команду 👇", reply_markup=markup)
        await state.set_state("settings")
    elif command in ["📞 Aloqa va manzillar", "📞 Contact and addresses", "📞 Контакты и адреса"]:
        lang = await get_lang(message.from_user.id)
        markup = await about_menu(lang)
        if lang == "uz":
            await message.answer("Aloqa uchun raqamlar\n+998999410325\n+998999410325\nBizni ijtimoiy tarmoqlarda kuzating 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Contact numbers\n+998999410325\n+998999410325\nFollow us on social networks 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Контактные телефоны\n+998999410325\n+998999410325\nПодпишитесь на нас в социальных сетях 👇", reply_markup=markup)
    elif command in ["ℹ️ Biz haqimizda", "ℹ️ About us", "ℹ️ О нас"]:
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer(text="Biz keramika sohasidagi korxonamiz. 2005 yildan beri faoliyatimizni yuritamizBizdan kerkli maxsulotlar xariq qilishingiz mumkin.", reply_markup=markup)
        elif lang == "ru":
            await message.answer(text="Мы предприятие в области керамики. Мы работаем с 2005 года. У нас вы можете купить специальные товары.", reply_markup=markup)
        elif lang == "en":
            await message.answer(text="We are an enterprise in the field of ceramics. We have been operating since 2005. You can buy special products from us.", reply_markup=markup)
    elif command in ["🛍 Mahsulotlar", "🛍 Products", "🛍 Продукты"]:
        markup = await category_keyboard(lang)
        if lang == "uz":
            await message.answer("Kerakli maxsulot kategoriyasini tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Choose a product category 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите категорию товара 👇", reply_markup=markup)
        await state.update_data(order_type=order_type)
        await state.set_state("get_category")
    elif command in ["💎 Bonus", "💎 Бонус"]:
        markup = await user_menu(lang)
        link = await get_start_link(f'{message.from_user.id}', encode=True)
        user = await get_user(message.from_user.id)
        user.referal = link
        user.save()
        text = ""
        if lang == "uz":
           text = f"Bonusga ega bo'lish uchun 2xil usul mavjud:\n\n1) Tanga to'plash, Ya'ni har 1millionlik savdo uchun 1tanga\n2)Referal orqali do'stingizni taklif qilib, uning 1-xaridi 5mlnni tashkil qilsa sizga 1 tanga beriladi\n\nSizning referal havolangiz: {link}"
        if lang == "en":
            text = f"There are 2 ways to get a bonus:\n\n1) Accumulating coins, that is, 1 coin for every 1 million sales\n2) You will get 1 coin if you invite your friend through referral and his 1st purchase is 5 million will be given\n\nYour referral link: {link}"
        if lang == "ru":
            text = f"Есть 2 способа получить бонус:\n\n1) Накопление монет, то есть 1 монета за каждый 1 миллион продаж\n2) Вы получите 1 монету, если пригласите своего друга по рефералу и его 1-я покупка составит 5 миллионов будет предоставлена\n\nВаша реферальная ссылка: {link}"
        await message.answer(text = text, reply_markup=markup)
        await state.set_state("get_command")
    elif command in ["💰 Keshbeklar haqida ma'lumot", "💰 Information about cashbacks", "💰 Информация о кэшбэках"]:
        user = await get_user(message.from_user.id)
        coins = user.coins
        markup = await user_menu(lang) 
        if lang == "uz":
            await message.answer(f"Sizda hozirda {coins} tanga bor.\nTangani qanday ishkatishni tez orada hal qilamiz", reply_markup=markup)
        if lang == "ru":
            await message.answer(f"В настоящее время у вас есть {coins} монет.\nСкоро мы решим, как добывать монету.", reply_markup=markup)
        if lang == "en":
            await message.answer(f"You currently have {coins} coins.\nWe will decide how to mine the coin soon", reply_markup=markup)
    elif command in ["🗂 Buyurtmalar tarixi", "🗂 Order history", "🗂 История заказов"]:
        summa = 0
        orders = await get_orders(message.from_id)
        if lang =="uz":
            text = "<b>🛒Sizning Buyurtmalaringiz tarixi</b>\n\n"
        elif lang =="en":
            text = "<b>🛒Your Order History</b>\n\n"
        elif lang =="ru":
            text = "<b>🛒История ваших заказов</b>\n\n"
            
        for order in orders:  
            order_details = await get_order_details(order.id)      
            if lang == "uz":
                text += f"🆔 Buyurtma: <b>#{order.id}</b>\n"\
                f"🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n"
                for order_detail in order_details:
                    text += f"  {order_detail.product.category.name_uz}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"\n<b>Jami: </b>{summa}\n\n"
            elif lang == "ru":
                text += f"<b>🛒Заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\n"\
                f"🕙Время заказа: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Адрес: {order.address}\n"
                for order_detail in order_details:
                    text += f"  {order_detail.product.category.name_ru}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"\n<b>Jami: </b>{summa}\n\n"
            elif lang == "en":
                text = f"<b>🛒Your Order</b>\n\n🆔 Order: <b>#{order.id}</b>\n"\
                f"🕙Order date: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Address: {order.address}\n"
                for order_detail in order_details:
                    text += f"  {order_detail.product.category.name_en}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"\n<b>Jami: </b>{summa}\n\n"
        await message.answer(text)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state="settings")
async def get_settings_message(message: types.Message, state:FSMContext):
    lang = await get_lang(message.from_user.id)
    if "⬅️" in  message.text:
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Select the required button👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите нужную кнопку👇", reply_markup=markup)
        await state.set_state("get_command")
    elif message.text in ["🔄 Tilni o'zgartirish", "🔄 Изменить язык", "🔄 Change language"]:
        if lang == "uz":
            markup = await language_keyboard()
            await message.answer(text="Tilni o'zgartirish ♻️\nKerakli tilni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            markup = await language_keyboard()
            await message.answer(text="Change language ♻️\nChoose the language you want 👇", reply_markup=markup)
        elif lang == "ru":
            markup = await language_keyboard()
            await message.answer(text="Изменить язык ♻️\nВыберите нужный язык 👇", reply_markup=markup)
        await state.set_state("set_lang")
    elif message.text in ["📞 Raqamni o'zgartirish", "📞 Изменить номер телефона", "📞 Change phone number"]:
        markup = await phone_keyboard(lang)
        if lang == "uz":
            await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Enter your phone number in international format (<b>998YYXXXXXX</b>). Or share the number 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
        await state.set_state("get_phone_number_settings")            


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state="get_phone_number_settings")
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number[1:]
        user = await get_user(message.from_user.id)
        user.new_phone = phone
        otp = generateOTP()
        send_sms(otp=otp, phone=phone)
        user.otp = otp
        user.save()
        print(user.otp)
        lang = await get_lang(message.from_user.id)
        keyboard = await back_keyboard(lang)
        if lang == "uz":
            await message.answer(text=f"<b>{user.new_phone}</b> raqamiga yuborilgan tasdiqlash kodini kiriting", parse_mode='HTML', reply_markup=keyboard)
        if lang == "ru":
            await message.answer(text=f"Введите код подтверждения, отправленный на номер <b>{user.new_phone}</b>.", parse_mode='HTML', reply_markup=keyboard)
        if lang == "en":
            await message.answer(text=f"Enter the verification code sent to <b>{user.new_phone}</b>", parse_mode='HTML', reply_markup=keyboard)
        await state.set_state("get_otp_settings")
    

@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_phone_number_settings")
async def get_phone_settings(message: types.Message, state: FSMContext):
    if "⬅️" not in message.text:
        lang = await get_lang(message.from_user.id)
        if isValid(message.text):
            phone = message.text
            user = await get_user(message.from_user.id)
            user.new_phone = phone
            otp = generateOTP()
            send_sms(otp=otp, phone=phone)
            user.otp = otp
            user.save()
            print(user.otp)
            keyboard = await back_keyboard(lang)
            if lang == "uz":
                await message.answer(text=f"<b>{user.new_phone}</b> raqamiga yuborilgan tasdiqlash kodini kiriting", parse_mode='HTML', reply_markup=keyboard)
            if lang == "en":
                await message.answer(text=f"Введите код подтверждения, отправленный на номер <b>{user.new_phone}</b>.", parse_mode='HTML', reply_markup=keyboard)
            if lang == "ru":
                await message.answer(text=f"Enter the verification code sent to <b>{user.new_phone}</b>", parse_mode='HTML', reply_markup=keyboard)
            await state.set_state("get_otp_settings")
        else:
            markup = await phone_keyboard(lang)
            if lang == "uz":
                await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
            elif lang == "en":
                await message.answer("Enter your phone number in international format (<b>998YYXXXXXX</b>). Or share the number 👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
            await state.set_state("get_phone_number_settings")            
    else:
        lang = await get_lang(message.from_user.id)
        # if message.text == "⬅️️  Назад" or message.text == "⬅️️  Orqaga" or message.text == "⬅️️  Back":
        markup = await settings_keyboard(lang)
        if lang == "uz":
            await message.answer(text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer(text="Click the required button 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer(text="Выберите нужную команду 👇", reply_markup=markup)
        await state.set_state("settings")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_otp_settings")
async def get_phone(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user.lang
    if "⬅️️" in message.text: 
        markup = await phone_keyboard(lang)
        if lang == "uz":
            await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Enter your phone number in international format (<b>998YYXXXXXX</b>). Or share the number 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
        await state.set_state("get_phone_number_settings")            
    else:
        if message.text == user.otp:
            user.phone = user.new_phone
            user.save()
            markup = await settings_keyboard(lang)
            if lang == "uz":
                await message.answer("✅ Telefon raqami o'zgartirildi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
            elif lang == "en":
                await message.answer("✅Phone number has been changed. Choose the section you want👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("✅ Номер телефона изменен. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
            await state.set_state("settings")
        else:
            lang = await get_lang(message.from_user.id)
            markup = await back_keyboard(lang)
            if lang == "uz":
                await message.answer("⚠️ Yuborilgan tasdiqlash kodi xato. Qayta urinib ko'ring", reply_markup=markup)
            elif lang == "en":
                await message.answer("⚠️ The verification code sent is incorrect. Try again", reply_markup=markup)
            elif lang == "ru":
                await message.answer("⚠️ Присланный проверочный код неверный. Попробуйте еще раз", reply_markup=markup)
            await state.set_state("get_otp_settings")
 
 
@dp.message_handler(state="set_lang")
async def set_language(message: types.Message, state: FSMContext):
    data = message.text
    user = await get_user(message.from_user.id)
    if message.text == "🇺🇿 O'zbek tili":
        data = "uz"
    elif message.text == "🇺🇸 English":
        data = "en"
    elif message.text == "🇷🇺 Русский язык":
        data = "ru"
    user.lang = data
    user.save()
    lang = await get_lang(message.from_user.id)
    markup = await settings_keyboard(lang)
    if lang == "uz":
        await message.answer("Til o'zgariltirildi ✅.\nKerakli bo'limni tanlang 👇", reply_markup=markup)
    elif lang == "en":
        await message.answer("The language has been changed ✅.\nClick the required button 👇", reply_markup=markup)
    elif lang == "ru":
        await message.answer("Язык изменен ✅.\nНажмите нужную кнопку👇", reply_markup=markup)
    await state.set_state("settings")


@dp.message_handler(state="get_feedback")
async def get_feedback_message(message: types.Message, state:FSMContext):
    if message.text in ["⬅️ Orqaga", "⬅️ Back", "⬅️ Назад"]:
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Choose the required button👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите нужную кнопку👇", reply_markup=markup)
        await state.set_state("get_command")
    else:
        await message.forward(chat_id=-1001570855404)
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Fikr-mulohazangiz uchun tashakkur!", reply_markup=markup)
        elif lang == "en":
            await message.answer("Thanks for your feedback!", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Спасибо за ваш отзыв!", reply_markup=markup)
        await state.set_state("get_command")

    
@dp.callback_query_handler(state="get_category")
async def get_category(call: types.CallbackQuery, state:FSMContext):
    data = call.data 
    lang = await get_lang(call.from_user.id)
    if data == "back":
        await call.message.delete()
        markup = await user_menu(lang)
        if lang == "uz":
            await bot.send_message(chat_id=call.from_user.id, text="Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await bot.send_message(chat_id=call.from_user.id, text="Select the required button 👇", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=call.from_user.id, text="Выберите нужную кнопку 👇", reply_markup=markup)
        await state.set_state("get_command")
    else:
        markup = await subcategory_keyboard(lang=lang, cat_id=data)
        text = ""
        if lang == "uz":
            text = "Kerakli bo'limni tanlang 👇"
        if lang == "en":
            text = "Choose the desired section 👇"
        if lang == "ru":
            text = "Выберите нужную кнопку 👇"
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state("get_subcategory")

    
@dp.callback_query_handler(state="get_subcategory")
async def get_category(call: types.CallbackQuery, state:FSMContext):
    data = call.data 
    lang = await get_lang(call.from_user.id)
    if data == "back":
        await call.message.delete()
        markup = await user_menu(lang)
        if lang == "uz":
            await bot.send_message(chat_id=call.from_user.id, text="Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await bot.send_message(chat_id=call.from_user.id, text="Select the required button 👇", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=call.from_user.id, text="Выберите нужную кнопку 👇", reply_markup=markup)
        await state.set_state("get_command")
    else:
        markup = await product_keyboard(lang=lang, cat_id=data)
        category = await get_subcategory(data)
        await state.update_data(subcategory_id=category.id)
        await call.message.delete()
        text = ""
        photo = open(f'.{category.ImageURL}', 'rb') 
        if lang == "uz":
            text = "Kerakli maxsulotni tanlang 👇"
        if lang == "en":
            text = "Choose the desired product 👇"
        if lang == "ru":
            text = "Выберите нужный товар 👇"
        await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=markup)
        await state.set_state("get_product")


@dp.callback_query_handler(state="get_product")
async def get_category(call: types.CallbackQuery, state:FSMContext):
    data = call.data 
    lang = await get_lang(call.from_user.id)
    if data == "back":
        await call.message.delete()
        markup = await category_keyboard(lang)
        if lang == "uz":
            await bot.send_message(chat_id=call.from_user.id, text="Kerakli maxsulot kategoriyasini tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await bot.send_message(chat_id=call.from_user.id, text="Choose a product category 👇", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=call.from_user.id, text="Выберите категорию товара 👇", reply_markup=markup)
        await state.set_state("get_category")
    else:
        product = await get_product(data)
        await call.message.delete()
        await state.update_data(product_id=data)
        markup = await massa_keyboard(lang=lang, product_id=product.id)
        if product.image:
            photo = open(f'.{product.ImageURL}', 'rb')
            weihgts = await get_weihgts(product.id)
            await state.update_data(color_id=data)
            text = ""
            if lang == "uz":
                text = f"{product.subcategory.name_uz} model {product.name}. Mavjud grammlar: \n{weihgts}. Kerakli miqdorni tanlang 👇"
            if lang == "en":
                text = f"{product.subcategory.name_en} model {product.name}. Available grams: \n{weihgts}. Select the required amount 👇"
            if lang == "ru":
                text = f"{product.subcategory.name_en} модель {product.name}. Доступные граммы: \n{weihgts}. Выберите необходимое количество 👇"
            await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=markup)
        else:
            await bot.send_message(chat_id=call.from_user.id, text=text, rely_markup=markup) 
        await state.set_state("get_massa")  
            

@dp.callback_query_handler(state="get_massa")
async def get_category(call: types.CallbackQuery, state:FSMContext):
    data = call.data 
    lang = await get_lang(call.from_user.id)
    state_data = await state.get_data()
    product_id = state_data['product_id']
    product = await get_product(product_id)
    if data == "back":
        product = await get_product(product_id)
        await call.message.delete()
        subcategory_id = state_data["subcategory_id"]
        markup = await product_keyboard(lang=lang, cat_id=subcategory_id)
        category = await get_subcategory(subcategory_id)
        text = ""
        photo = open(f'.{category.ImageURL}', 'rb') 
        if lang == "uz":
            text = "Kerakli maxsulotni tanlang 👇"
        if lang == "en":
            text = "Choose the desired product 👇"
        if lang == "ru":
            text = "Выберите нужный товар 👇"
        await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=markup)
        await state.set_state("get_product")

    else:
        await state.update_data(massa_id=data)
        product = await get_product(product_id)
        massa = product.weihgts.filter(id=data).first()
        markup = await buy_keyboard(lang)
        text = ""
        price = massa.massa * product.price
        if lang == "uz":
            text = f"{product.subcategory.name_uz} model {product.name}.\nMiqdor: {massa.massa} gr\nNarxi: {price}"
        if lang == "ru":
            text = f"{product.subcategory.name_ru} model {product.name}.\nКоличество: {massa.massa} гр\nЦена: {price}"
        if lang == "en":
            text = f"{product.subcategory.name_en} model {product.name}.\nAmount: {massa.massa} gr\nPrice: {price}"
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)

        await state.set_state("buy_or_back")
        

@dp.message_handler(state="buy_or_back")
async def buy_or_back(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    state_data = await state.get_data()
    product_id = state_data['product_id']
    color_id = state_data['color_id']
    color = await get_color(color_id)
    product = await get_product(product_id)
    if message.text in ["🛒 Sotib olish", "🛒 Buy", "🛒 Купить"]:
        markup = await order_type(lang)
        if lang == "uz":
            await bot.send_message(chat_id=message.from_user.id, text="Xizmat turini tanlang", reply_markup=markup)
        elif lang == "en":
            await bot.send_message(chat_id=message.from_user.id, text="Select the type of service", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=message.from_user.id, text="Выберите тип услуги", reply_markup=markup)
        await state.set_state("get_service_type")
    elif message.text in ["⬅️ Orqaga", "⬅️ Back", "⬅️ Назад"]:
        weihgts = await get_weihgts(product_id)
        markup = await massa_keyboard(lang=lang, product_id=product_id)
        text = ""
        if lang == "uz":
            text = f"{product.subcategory.name_uz} model {product.name}. Mavjud grammlar: \n{weihgts}. Kerakli miqdorni tanlang 👇"
        if lang == "en":
            text = f"{product.subcategory.name_en} model {product.name}. Available grams: \n{weihgts}. Select the required amount 👇"
        if lang == "ru":
            text = f"{product.subcategory.name_en} модель {product.name}. Доступные граммы: \n{weihgts}. Выберите необходимое количество 👇"
        if product.image:
            photo = open(f'.{product.ImageURL}', 'rb')
            await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=text, reply_markup=markup)
        else:
            await bot.send_message(chat_id=message.from_user.id, text=text, rely_markup=markup)
        
        await state.set_state("get_massa")  
        

    
@dp.message_handler(state="get_command_about")
async def get_command_about(message: types.Message, state: FSMContext):
    if message.text in ["⬅️ Orqaga", "⬅️ Back", "⬅️ Назад"]:
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Choose the required button👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите нужную кнопку👇", reply_markup=markup)
        await state.set_state("get_command")


@dp.message_handler(state="get_service_type")
async def get_command_about(message: types.Message, state: FSMContext):
    user = await get_user(message.from_id)
    state_data = await state.get_data()
    product_id = state_data['product_id']
    product = await get_product(product_id)
    lang = await get_lang(message.from_user.id)
    if message.text in ["⬅ Назад", "⬅ Orqaga", "⬅ Back"]:
        weihgts = await get_weihgts(product_id)
        markup = await massa_keyboard(lang=lang, product_id=product_id)
        text = ""
        if lang == "uz":
            text = f"{product.subcategory.name_uz} model {product.name}. Mavjud grammlar: \n{weihgts}. Kerakli miqdorni tanlang 👇"
        if lang == "en":
            text = f"{product.subcategory.name_en} model {product.name}. Available grams: \n{weihgts}. Select the required amount 👇"
        if lang == "ru":
            text = f"{product.subcategory.name_en} модель {product.name}. Доступные граммы: \n{weihgts}. Выберите необходимое количество 👇"
        if product.image:
            photo = open(f'.{product.ImageURL}', 'rb')
            await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=text, reply_markup=markup)
        else:
            await bot.send_message(chat_id=message.from_user.id, text=text, rely_markup=markup)
        await state.set_state("get_massa")
    elif message.text in ["🏃‍♂️ Olib ketish", "🏃‍♂️ Самовывоз", "🏃‍♂️ Pick up"]:
        data = await state.get_data()
        order_type = "pick"
        user = await get_user(message.from_user.id)
        user.order_type = order_type
        user.save()
        product = data['product_id']
        gramm = data['massa_id']
        date = datetime.datetime.now()
        massa = await get_massa(gramm)
        order = await add_order(user_id=message.from_id, date=date, address="", gramm=gramm, product=product)
        await state.update_data(order_id=order.id, order_type=order_type)
        price = order.product.price * massa.massa
        cashback = user.cashback
        summa = price - cashback
        if lang == "uz":
            text = f"<b>🛒Sizning Buyurtmangiz</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
            f"👤 Xaridor: <b>#{order.user.user_id}</b>\nTelefon <b>+{order.user.phone}</b>\nBuyurtma: {order.product.subcategory.name_uz} {order.product.name} {order.gramm}\nBuyurtma turi: Tekkazib berish\n📍 Manzil: {order.address}\n"
            text += f"\n<b>Narxi: </b>{price} UZS  Keshbek {cashback} UZS\n Umumiy summa: {summa}"
            text += f"\nBuyurtmani tasdiqlang 👇"
        elif lang == "ru":
            text = f"<b>🛒Ваш заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\n"\
            f"👤 Заказчик: <b>#{order.user.user_id}</b>\nТелефон <b>+{order.user.phone}</b>\nЗаказ: {order.product.subcategory.name_uz} {order.product.name} {order.gramm}\nТип заказа: Доставка\n📍 Адрес: {order.address}\n"
            text += f"<b>Цена: </b>{price} сум Кэшбэк {cashback} сум\n Общая сумма: {summa}"
            text += f"\nПодтвердите заказ 👇"
        elif lang == "en":
            text = f"<b>🛒Your Order</b>\n\n🆔 Order: <b>#{order.id}</b>\n"\
            f"👤 Customer: <b>#{order.user.user_id}</b>\nPhone <b>+{order.user.phone}</b>\nOrder: {order.product.subcategory.name_uz} {order.product.name} {order.gramm}\nOrder Type: Delivery\n📍 Address: {order.address}\n"
            text += f"<b>Price: </b>{price} UZS Cashback {cashback} UZS\n Total amount: {summa}"
            text += f"\nConfirm the order 👇"
        order.summa = summa
        order.save()
        markup = await confirmation_keyboard(lang)
        await message.answer(text=text, reply_markup=markup)
        await state.set_state("confirm_order")
    elif message.text in ["🚚 Yetkazib berish", "🚚 Deliver", "🚚  Доставка"]:
        order_type = "deliver"
        user.order_type = order_type
        user.save()
        lang = await get_lang(message.from_user.id)
        text = []
        if lang == 'uz':
            text = ['Yetkazish manzilini jo\'nating']
        elif lang == 'ru':
            text = ['Отправьте адрес доставки']
        elif lang == 'en':
            text = ['Please send your delivery address']
        markup = await location_send(lang)
        await state.update_data(order_type=order_type)
        await message.answer(f"{text[0]} 👇", reply_markup=markup)
        await state.set_state("get_address")
    else:
        pass        
    

@dp.message_handler(state="get_payment_method")
async def get_count(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    data = await state.get_data()
    order_id = data["order_id"]
    user = await get_user(message.from_id)
    if message.text in ["⬅ Orqaga", "⬅ Back", "⬅ Назад"]:
        markup = await order_type(lang)
        if lang == "uz":
            await bot.send_message(chat_id=message.from_user.id, text="Xizmat turini tanlang", reply_markup=markup)
        elif lang == "en":
            await bot.send_message(chat_id=message.from_user.id, text="Select the type of service", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=message.from_user.id, text="Выберите тип услуги", reply_markup=markup)
        await state.set_state("get_service_type")
    elif message.text in ["🔵 Click", "🟢 Payme"]:
        card_type = ''
        if message.text == "🔵 Click":
            card_type = "click"
        elif message.text == "🟢 Payme":
            card_type = "payme"
        await state.update_data(card_type=card_type)
        order = await get_order(order_id)
        summa = order.summa
        prices = []
        if message.text == "🔵 Click":
            photo = 'https://click.uz/click/images/clickog.png'
            token = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'
        elif message.text == "🟢 Payme":
            photo = "https://cdn.paycom.uz/documentation_assets/payme_01.png"
            token = '371317599:TEST:1672062523890'
        prices.append(
            types.LabeledPrice(label=f"Test uchun tanish", amount=int(1000) * 100))
        await bot.send_invoice(chat_id=message.from_user.id, title=f'Test title',
                               description=f' Test description',
                               provider_token=token,
                               currency='UZS',
                               photo_url=photo,
                               photo_height=512,  # !=0/None or picture won't be shown
                               photo_width=512,
                               photo_size=512,
                               prices=prices,
                               start_parameter='hz-wto-tut',
                               payload="Payload"
                               )
        await state.set_state("payment")        
       
    elif message.text in ["💴 Naqd pul orqali", "💴 Наличными", "💴 Cash"]:
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("✅ Buyurtma qabul qilindi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("✅ Order received. Choose the section you want 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("✅ Заказ получен. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
        await state.set_state("get_command")
            


@dp.message_handler(content_types=types.ContentType.LOCATION, state='get_address')
async def get_location_address(message: types.Message, state: FSMContext):
    location = message.location
    geolocator = Nominatim(user_agent="geoapiExercises")
    Latitude = str(location.latitude)
    Longitude = str(location.longitude)
    location = geolocator.geocode(Latitude + "," + Longitude)
    data = location.raw.get('display_name')
    data = data.split(',')
    name = f"{data[0]} {data[1]} {data[2]}"
    user = await get_user(message.from_user.id)
    lang = user.lang
    text = []
    if lang == 'uz':
        text = '🔰 Manzilni tasdiqlaysizmi?'
    elif lang == 'ru':
        text = '🔰 Вы подтверждаете адрес?'
    elif lang == 'en':
        text = '🔰 Do you confirm the location?'
    await state.update_data(latitude=Latitude, longitude=Longitude, name=name,
                            display_name=location.raw.get('display_name'))
    await message.answer(text=location.raw.get('display_name'), reply_markup=ReplyKeyboardRemove())
    markup = await confirm_address(lang)
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
    await state.set_state('confirm_address')


@dp.message_handler(content_types=types.ContentType.TEXT, state='get_address')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    command = message.text
    if command in ['🔂 Oldingi manzillar', '🔂 Предыдущие адреса', '🔂 Previous addresses']:
        locations = await get_address(message.from_user.id)
        if locations:
            user = await get_user(message.from_user.id)
            lang = user.lang
            text = []
            if lang == 'uz':
                text = ['Kerakli mazilni tanlang', 'Manzillar']
            elif lang == 'ru':
                text = ['Выберите нужное место', 'Адреса']
            elif lang == 'en':
                text = ['Choose the desired mazil', 'Addresses']
            markup = await location_keys(user_id=message.from_user.id, lang=lang)
            await message.answer(text=text[1], reply_markup=ReplyKeyboardRemove())
            await bot.send_message(text=text[0], chat_id=message.from_user.id, reply_markup=markup)
            await state.set_state('get_location')
        else:
            user = await get_user(message.from_user.id)
            lang = user.lang
            text = []
            if lang == 'uz':
                text = '🗑 Manzillar ro\'yxati bo\'sh'
            elif lang == 'ru':
                text = '🗑 Список адресов пустой'
            elif lang == 'en':
                text = '🗑 The address list is empty'
            await message.answer(text)
    elif message.text in ["⬅ Orqaga", "⬅ Back", "⬅ Назад"]:
        markup = await order_type(lang)
        if lang == "uz":
            await bot.send_message(chat_id=message.from_user.id, text="Xizmat turini tanlang", reply_markup=markup)
        elif lang == "en":
            await bot.send_message(chat_id=message.from_user.id, text="Select the type of service", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=message.from_user.id, text="Выберите тип услуги", reply_markup=markup)
        await state.set_state("get_service_type")


@dp.message_handler(content_types=types.ContentType.TEXT, state='get_location')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    loc = message.text
    location = await get_location_by_name(name=loc, user_id=message.from_id)
    if location is not None:
        geolocator = Nominatim(user_agent="geoapiExercises")
        Latitude = str(location.latitude)
        Longitude = str(location.longitude)
        location = geolocator.geocode(Latitude + "," + Longitude)
        data = location.raw.get('display_name')
        data = data.split(',')
        name = f"{data[0]} {data[1]} {data[2]}"
        user = await get_user(message.from_user.id)
        lang = user.lang
        text = []
        if lang == 'uz':
            text = '🔰 Manzilni tasdiqlaysizmi?'
        elif lang == 'ru':
            text = '🔰 Вы подтверждаете адрес?'
        elif lang == 'en':
            text = '🔰 Do you confirm the location?'
        await state.update_data(latitude=Latitude, longitude=Longitude, name=name,
                                display_name=location.raw.get('display_name'))
        await message.answer(text=location.raw.get('display_name'), reply_markup=ReplyKeyboardRemove())
        markup = await confirm_address(lang)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
        await state.set_state('confirm_address')


@dp.message_handler(content_types=types.ContentType.TEXT, state='confirm_address')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    if message.text in ["⬅ Orqaga", "⬅ Back", "⬅ Назад"]:
        text = []
        if lang == 'uz':
            text = ['Yetkazish manzilini jo\'nating']
        elif lang == 'ru':
            text = ['Отправьте адрес доставки']
        elif lang == 'en':
            text = ['Please send your delivery address']
        markup = await location_send(lang)
        await message.answer(f"{text[0]} 👇", reply_markup=markup)
        await state.set_state("get_address")
    elif message.text in ["✅ Tasdiqlash", "✅ Подтвердить", "✅ Confirm"]:
        data = await state.get_data()
        user = await get_user(message.from_user.id)
        latitude = data['latitude']
        longitude = data['longitude']
        loc_name = data['name']
        address = data['display_name']
        product = data['product_id']
        gramm = data['massa_id']
        date = datetime.datetime.now()
        order = await add_order(user_id=message.from_id, date=date, address=address, gramm=gramm, product=product)
        await state.update_data(order_id=order.id)
        summa = order.product.price
        await add_address(latitude=latitude, longitude=longitude, user_id=message.from_user.id, name=loc_name)
        markup = await pay_method(lang)
        massa  = await get_massa(gramm)
        price = order.product.price * massa.massa
        cashback = user.cashback
        summa = price - cashback
        if lang == "uz":
            text = f"<b>🛒Sizning Buyurtmangiz</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
            f"👤 Xaridor: <b>#{order.user.user_id}</b>\nTelefon <b>+{order.user.phone}</b>\nBuyurtma: {order.product.category.name_uz} {order.gramm}\nBuyurtma turi: Yetkazib berish\n📍 Manzil: {order.address}\n"
            text += f"\n<b>Narxi: </b>{price} UZS  Keshbek {cashback} UZS\n Umumiy summa: {summa}"
            text += f"\nTo'lov turini tanlang 👇"
        elif lang == "ru":
            text = f"<b>🛒Ваш заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\n"\
            f"👤 Заказчик: <b>#{order.user.user_id}</b>\nТелефон <b>+{order.user.phone}</b>\nЗаказ: {order.product.category.name_uz} {order.gramm}\nТип заказа: Доставка\n📍 Адрес: {order.address}\n"
            text += f"<b>Цена: </b>{price} сум Кэшбэк {cashback} сум\n Общая сумма: {summa}"
            text += f"\nВыберите тип оплаты 👇"
        elif lang == "en":
            text = f"<b>🛒Your Order</b>\n\n🆔 Order: <b>#{order.id}</b>\n"\
            f"👤 Customer: <b>#{order.user.user_id}</b>\nPhone <b>+{order.user.phone}</b>\nOrder: {order.product.category.name_uz} {order.gramm}\nOrder Type: Delivery\n📍 Address: {order.address}\n"
            text += f"<b>Price: </b>{price} UZS Cashback {cashback} UZS\n Total amount: {summa}"
            text += f"\nSelect the payment type 👇"
        order.summa = summa
        order.save()
        await message.answer(text, reply_markup=markup)
        await state.set_state("get_payment_method")
    elif message.text in ["🔄 Qayta jo\'natish", "🔄 Отправить повторно", "🔄 Send again"]:
        lang = await get_lang(message.from_user.id)
        text = []
        if lang == 'uz':
            text = ['Yetkazish manzilini jo\'nating']
        elif lang == 'ru':
            text = ['Отправьте адрес доставки']
        elif lang == 'en':
            text = ['Please send your delivery address']
        markup = await location_send(lang)
        await message.answer(text=f"{text[0]} 👇", reply_markup=markup)
        await state.set_state("get_address")


@dp.message_handler(content_types=types.ContentType.TEXT, state='confirm_order')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    data = await state.get_data()
    if message.text in ["❌ Bekor qilish", "❌ Cancel", "❌ Отмена"]:
        await clear_cart(message.from_id)
        order_id = data['order_id']
        order = await get_order(order_id)
        order.delete()
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("❌ Buyurtma bekor qilindi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("❌ Заказ отменен. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("❌ The order has been cancelled. Please select the desired section 👇", reply_markup=markup)
        await state.set_state("get_command")
    elif message.text in ["✅ Подтвердить", "✅ Tasdiqlash", "✅ Confirm"]:
        order_type = data["order_type"]
        if order_type == "pick":
            markup = await user_menu(lang)
            user = await get_user(message.from_user.id)
            cash = 0
            order = get_order(data["order_id"])
            if order.summa >= 5000000:
                cash += order.summa * 0.03
            user.cashback = cash
            user.save()
            if lang == "uz":
                await message.answer("✅ Buyurtma qabul qilindi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
            elif lang == "en":
                await message.answer("✅ Order received. Choose the section you want 👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("✅ Заказ получен. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
            await state.set_state("get_command")
            
        # markup = await pay_method(lang)
        # if lang == "uz":
        #     await message.answer("Iltimos to'lov usulini tanlang 👇", reply_markup=markup)
        # elif lang == "en":
        #     await message.answer("Please select a payment method 👇", reply_markup=markup)
        # elif lang == "ru":
        #     await message.answer("Пожалуйста, выберите способ оплаты 👇", reply_markup=markup)
        # await state.set_state("get_payment_method")
        # prices = []
        # if card_type != "cash":
        #     if card_type == "click":
        #         photo = 'https://click.uz/click/images/clickog.png'
        #         token = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'
        #     elif message.text == "payme":
        #         photo = "https://cdn.paycom.uz/documentation_assets/payme_01.png"
        #         token = '371317599:TEST:1666271002702'
        #     prices.append(
        #         types.LabeledPrice(label=f"Test uchun tanish", amount=int(1000) * 100))
        #     await bot.send_invoice(chat_id=message.from_user.id, title=f'Test title',
        #                         description=f' Test description',
        #                         provider_token=token,
        #                         currency='UZS',
        #                         photo_url=photo,
        #                         photo_height=512,  # !=0/None or picture won't be shown
        #                         photo_width=512,
        #                         photo_size=512,
        #                         prices=prices,
        #                         start_parameter='hz-wto-tut',
        #                         payload="Payload"
        #                         )
        #     await state.set_state("payment") 
        # else:   
        #     await clear_cart(message.from_id)
        #     markup = await user_menu(lang)
        #     if lang == "uz":
        #         await message.answer("✔️ Buyurtma muvaffaqiyatli amalga oshirildi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        #     elif lang == "ru":
        #         await message.answer("✔️ Корзина очищена. Выберите нужный раздел👇", reply_markup=markup)
        #     elif lang == "en":
        #         await message.answer("✔️ Cart cleared. Please select the desired section 👇", reply_markup=markup)
        #     await state.set_state("get_command")
                   
        

@dp.pre_checkout_query_handler(lambda query: True, state='payment')
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT, state="payment")
async def got_payment(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    data = await state.get_data()
    await clear_cart(message.from_id)
    user = await get_user(message.from_user.id)
    cash = 0
    order = get_order(data["order_id"])
    if order.summa >= 5000000:
        cash += order.summa * 0.03
    user.cashback = cash
    user.save()
    markup = await user_menu(lang)
    if lang == "uz":
        await message.answer("✅ Buyurtma qabul qilindi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
    elif lang == "en":
        await message.answer("✅ Order received. Choose the section you want 👇", reply_markup=markup)
    elif lang == "ru":
        await message.answer("✅ Заказ получен. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
    await state.set_state("get_command")
