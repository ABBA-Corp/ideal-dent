from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *
from utils.db_api.database import *


# async def language_keyboard():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#             InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="uz"),
#             InlineKeyboardButton(text="🇺🇸 English", callback_data="en"),
#             InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="ru")
#             ]
#             ])
#     return markup


# async def user_menu(lang):
#     texts = []
#     if lang == "uz":
#         texts = ["Menyu", "Sozlamalar", "Fikr qoldirish", "Biz haqimizda"]
#     elif lang == "en":
#         texts = ["Menu", "Settings", "Feedback", "About us"]
#     elif lang == "ru":
#         texts = ["Меню", "Настройки", "Отзыв", "О нас"]
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text=f"🛒 {texts[0]}", callback_data="menu")],
#             [InlineKeyboardButton(text=f"⚙️ {texts[1]}", callback_data="settings")],
#             [InlineKeyboardButton(text=f"💬 {texts[2]}", callback_data="feedback")],
#             [InlineKeyboardButton(text=f"📑 {texts[3]}", callback_data="about")],
#         ]
#     )
#     return markup


# async def back_keyboard(lang):
#     texts = []
#     if lang == "uz":
#         texts = ["Orqaga"]
#     elif lang == "en":
#         texts = ["Back"]
#     elif lang == "ru":
#         texts = ["Назад"]
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text=f"⬅️ {texts[0]}", callback_data="back")],
#         ]
#     )
#     return markup


async def about_menu(lang):
    texts = []
    if lang == "uz":
        texts = ["Telegram", "Facebook", "Youtube", "Instagram", "Orqaga"]
    elif lang == "en":
        texts = ["Telegram", "Facebook", "Youtube", "Instagram", "Back"]
    elif lang == "ru":
        texts = ["Телеграм", "Facebook", "Youtube", "Instagram", "Назад"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{texts[0]}", url="http://t.me/DunyaBunya")],
            [InlineKeyboardButton(text=f"{texts[1]}", url="https://www.facebook.com/dunyabunya.uz")],
            [InlineKeyboardButton(text=f"{texts[2]}", url="https://youtube.com/")],
            [InlineKeyboardButton(text=f" {texts[3]}", url="https://instagram.com/")],
        ]
    )
    return markup


async def go_search(lang):
    texts = []
    if lang == "uz":
        texts = ["Izlash"]
    elif lang == "en":
        texts = ["Search"]
    elif lang == "ru":
        texts = ["Поиск"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🔎 {texts[0]}", switch_inline_query_current_chat=""),
            ],
        ]
    )
    return markup


async def go_order(lang):
    texts = []
    if lang == "uz":
        texts = ["Xaridni boshlash"]
    elif lang == "en":
        texts = ["Start shopping"]
    elif lang == "ru":
        texts = ["Начать покупки"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🛍 {texts[0]} ↗️", callback_data="go_shopping")],
        ]
    )
    return markup


# async def subcategory_keyboard(lang, cat_id):
#     texts = []
#     sub_categories = SubCategory.objects.filter(category_id=cat_id).all()
#     inline_keyboard = []
#     for i in sub_categories:
#         if lang == "uz":
#             inline_keyboard.append([InlineKeyboardButton(text=f"{i.name_uz}", callback_data=i.id)])
#             texts = ["Orqaga"]
#         elif lang == "en":
#             inline_keyboard.append([InlineKeyboardButton(text=f"{i.name_en}", callback_data=i.id)])
#             texts = ["Back"]
#         elif lang == "ru":
#             texts = ["Назад"]
#             inline_keyboard.append([InlineKeyboardButton(text=f"{i.name_ru}", callback_data=i.id)])
#     inline_keyboard.append([InlineKeyboardButton(text=f"🔙 {texts[0]}", callback_data=f"back-{cat_id}")])
#     markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
#     return markup


# async def product_keyboard(lang, sub_id):
#     texts = ''
#     products = Product.objects.filter(sub_category__id=sub_id).all()
#     inline_keyboard = []
#     for i in products:
#         if lang == "uz":
#             inline_keyboard.append([InlineKeyboardButton(text=f"{i.name_uz}", callback_data=i.id)])
#             texts = "Orqaga"
#         elif lang == "en":
#             inline_keyboard.append([InlineKeyboardButton(text=f"{i.name_en}", callback_data=i.id)])
#             texts = "Back"
#         elif lang == "ru":
#             inline_keyboard.append([InlineKeyboardButton(text=f"{i.name_ru}", callback_data=i.id)])
#             texts = "Назад"
#     inline_keyboard.append([InlineKeyboardButton(text=f"🔙 {texts}", callback_data=f"back-{sub_id}")])
#     markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
#     return markup

async def order_keyboard(cart_id, lang):
    texts = []
    if lang == "uz":
        texts = ["Savatchaga qo'shish", "Orqaga"]
    elif lang == "en":
        texts = ["Add to card", "Back"]
    elif lang == "ru":
        texts = ["Добавить в корзину", "Назад"]

    markup = InlineKeyboardMarkup(row_width=3)
    cart = CartObject.objects.filter(id=cart_id).first()
    markup.insert(
        InlineKeyboardButton(text=f"➖", callback_data=f"cart_minus-{cart.id}"))
    markup.insert(
        InlineKeyboardButton(text=f"{cart.count}", callback_data="no_call-1"))
    markup.insert(
        InlineKeyboardButton(text=f"➕", callback_data=f"cart_plus-{cart.id}"))
    markup.row(InlineKeyboardButton(text=f"📥 {texts[0]} ", callback_data=f"confirm-{cart.id}"))
    markup.row(InlineKeyboardButton(text="⬅️ Back ", callback_data=f"cancel-{cart.id}"))
    return markup



# async def back_admin_menu():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_admin"),
#             ],
#         ]
#     )
#     return markup


# async def doctor_in_admin():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="🗓 Bugungi kungi keshbekni ko'rish", callback_data="kash_today")],
#             [InlineKeyboardButton(text="📅 Alohida kun uchun keshbekni ko'rish", callback_data="kash_day")],
#             [InlineKeyboardButton(text="📆 Shu oy uchun keshbekni ko'rish", callback_data="kash_this_month")],
#             [InlineKeyboardButton(text="🗒 Alohida oy uchun keshbekni ko'rish", callback_data="kash_month")],
#             [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_admin")],
#         ]
#     )
#     return markup


# async def back_keyboard():
#     keyboard = ReplyKeyboardMarkup()
#     key1 = KeyboardButton(text="⬅️ Bekor qilish")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard


# async def ask_keyboard():
#     keyboard = ReplyKeyboardMarkup()
#     key1 = KeyboardButton(text="💵 Avans so'rash")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard


# async def admin_menu():
#     keyboard = ReplyKeyboardMarkup(row_width=2)
#     key1 = KeyboardButton(text="Eslatma qo'shish")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard

# async def client_keys():
#     keyboard = ReplyKeyboardMarkup(row_width=2)
#     key1 = KeyboardButton(text="Keyingi to'lovni ko'rish")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard
