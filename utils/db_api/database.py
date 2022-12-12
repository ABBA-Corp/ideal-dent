from typing import List, Any
from asgiref.sync import sync_to_async
from backend.models import *
import random
import datetime 
from datetime import timedelta


@sync_to_async
def add_user(user_id, referal_user):
    try:
        user, created = User.objects.get_or_create(user_id=user_id)
        if user.referal_user:
            pass
        else:
            user.referal_user = referal_user
        user.save()
        return user
    except Exception as exx:
        print(exx)
        return None
    
@sync_to_async
def get_user(user_id):
    try:
        user = User.objects.filter(user_id=user_id).first()
        return user    
    except:
        return None

@sync_to_async
def get_lang(user_id):
    try:
        user = User.objects.filter(user_id=user_id).first()
        return user.lang
    except Exception as exx:
        print(exx)
        return None

@sync_to_async
def get_subcategory(sub_id):
    try:
        subcategory = SubCategory.objects.filter(id=sub_id).first()
        return subcategory
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_product(product_id):
    try:
        product = Product.objects.filter(id=product_id).first()
        return product
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def add_cart(user, product):
    try:
        cart, created = CartObject.objects.get_or_create(
            user=user,
            product=product
        )
        cart.save()
        return cart
    except Exception as exx:
         print(exx)
         return None


@sync_to_async
def get_cart(cart_id):
    try:
        cart = CartObject.objects.filter(id=cart_id).first()
        return cart
    except Exception as exx:
        print(exx)
        return None


@sync_to_async 
def get_category_by_name(name):
    try:
        categories = Category.objects.all()
        category = []
        for i in categories:
            if i.name_en == name or i.name_ru == name or i.name_uz == name:
                category = i
        return category
    except Exception as exx:
        print(exx)
        return None


@sync_to_async 
def get_subcategory_by_name(name):
    try:
        categories = SubCategory.objects.all()
        category = []
        for i in categories:
            if i.name_en == name or i.name_ru == name or i.name_uz == name:
                category = i
        return category
    except Exception as exx:
        print(exx)
        return None


@sync_to_async 
def get_product_by_name(name):
    try:
        products = Product.objects.all()
        product = []
        for i in products:
            if i.name_en == name or i.name_ru == name or i.name_uz == name:
                product = i
        return product
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_carts(user_id):
    try:
        user = User.objects.filter(user_id=user_id).first()
        summa = 0
        carts = CartObject.objects.filter(user=user).all()
        text = ''
        if user.lang == "uz":
            text = "<b>Savatchangiz:</b>\n\n"
            if carts:
                for cart in carts:
                    text += f"<b>{cart.count}</b>✖️ {cart.product.name_uz}\n"
                    summa += int(cart.count) * int(cart.product.price)    
                text += f"Jami: {summa} SUM"
            else:
                text += "⚠️ Hozircha savatingiz bo'sh"
        elif user.lang == "ru":
            text = "<b>Ваша корзина для покупок:</b>\n\n"
            if carts:
                for cart in carts:
                    text += f"<b>{cart.count}</b>✖️ {cart.product.name_ru}\n"
                    summa += int(cart.count) * int(cart.product.price)    
                text += f"Всего: {summa} СУМ"
            else:
                text += "⚠️ Ваша корзина пуста"
        elif user.lang == "en":
            text = "<b>Your shopping cart:</b>\n\n"
            if carts:
                for cart in carts:
                    text += f"<b>{cart.count}</b>✖️ {cart.product.name_en}\n"
                    summa += int(cart.count) * int(cart.product.price)    
                text += f"Total: {summa} SUM"
            else:
                text += "⚠️ Your cart is currently empty"
        return text
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_cart_objects(user_id):
    cards = CartObject.objects.filter(user__user_id=user_id)
    return cards


@sync_to_async
def get_orders(user_id):
    try:
        user = User.objects.filter(user_id=user_id).first()
        orders = Order.objects.filter(user=user).all()
        return orders
    except:
        return None
    

@sync_to_async
def get_products(product_name):
    try:
        products = Product.objects.all()
        product = []
        for i in products:
            if  product_name.lower() in i.name_en.lower()  or product_name.lower() in i.name_ru.lower() or product_name.lower() in i.name_uz.lower():
                product.append(i)
        return product
    except:
        return ""
        


@sync_to_async
def check_cart(user_id):
    try:
        user = User.objects.filter(user_id=user_id).first()
        carts = CartObject.objects.filter(user=user).all()
        if carts:
            return True
        else:
            return None
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def clear_cart(user_id):
    try:
        carts = CartObject.objects.filter(user__user_id=user_id).all()
        for cart in carts:
            cart.delete()
        return True
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def delete_cart_item(product, user_id):
    try:
        user = User.objects.filter(user_id=user_id).first()
        carts = CartObject.objects.filter(user=user, product=product).all()
        for cart in carts:
            cart.delete()
        return True
    except Exception as exx:
        print(exx)
        return None
    

@sync_to_async
def get_address(user_id):
    try:
        locs = Location.objects.filter(user_id=user_id).all()
        return locs
    except:
        return None

@sync_to_async
def add_address(longitude, latitude, name, user_id):
    try:
        long, created = Location.objects.get_or_create(longitude=longitude, latitude=latitude,
                                                       user_id=user_id, name=name)
        long.save()
        return long
    except:
        return None


@sync_to_async
def add_order(user_id, date, address):
    try:
        user = User.objects.filter(user_id=user_id).first()
        order, created = Order.objects.get_or_create(user=user, date=date, address=address)
        order.save()
        return order
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def add_order_detail(order_id, product_id, count):
    try:
        product = Product.objects.filter(id=product_id).first()
        order = Order.objects.filter(id=order_id).first()
        order_object, created = OrderDetail.objects.get_or_create(order=order, product=product, count=count)
        order_object.save()
        return order_object
    except Exception as exx:
        print(exx)
        return None
    
    
@sync_to_async
def get_order_details(order_id):
    try:
        order_objects = OrderDetail.objects.filter(order__id=order_id)
        return order_objects
    except:
        return None
    
    
@sync_to_async
def get_order(order_id):
    try:
        order = Order.objects.filter(id=order_id).first()
        return order
    except:
        return None
    
    
@sync_to_async
def get_location_by_name(user_id, name):
    try:
        locations = Location.objects.filter(user_id=user_id, name=name).first()
        return locations
    except Exception as exx:
        print(exx)
        return None
    
