from django.db import models
import random 


def generateunique() -> str:
    return random.randint(1000000, 9999999)


class User(models.Model):
    user_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    lang = models.CharField(max_length=20, null=True, blank=True)
    order_type = models.CharField(max_length=25, null=True, blank=True)


class Category(models.Model):
    name_uz = models.CharField(max_length=500, null=True, blank=True)
    name_en = models.CharField(max_length=500, null=True, blank=True)
    name_ru = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name_uz
        
    @property
    def ImageURL(self):
        try:
            return self.image.url
        except:
            return ''


class SubCategory(models.Model):
    name_uz = models.CharField(max_length=500, null=True, blank=True)
    name_en = models.CharField(max_length=500, null=True, blank=True)
    name_ru = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name_uz
    
    @property
    def ImageURL(self):
        try:
            return self.image.url
        except:
            return ''


class Product(models.Model):
    name_uz = models.CharField(max_length=500, null=True, blank=True)
    name_en = models.CharField(max_length=500, null=True, blank=True)
    name_ru = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name_uz
    
    @property
    def ImageURL(self):
        try:
            return self.image.url
        except:
            return ''
    

class Order(models.Model):
    PAY_CHOISE = [
        ("Payme", 'payme'),
        ("Click", 'click'),
        ("Cash", 'cash'),
    ]

    id = models.CharField(
        max_length=30,
        primary_key=True,
        default=generateunique,
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=False)
    summa = models.IntegerField(default=0)
    pay_type = models.CharField(max_length=10, null=True, blank=True, choices=PAY_CHOISE)
    address = models.CharField(max_length=200, null=True, blank=True)
    service_type = models.CharField(max_length=25, null=True, blank=True)
    paind = models.BooleanField(default=False)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()


class CartObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)    
    confirm = models.BooleanField(default=False)


class Location(models.Model):
    user_id = models.CharField(max_length=400, verbose_name="User id", null=True)
    name = models.CharField(max_length=400, verbose_name="Name")
    longitude = models.CharField(max_length=400, verbose_name="Longitude")
    latitude = models.CharField(max_length=400, verbose_name="Latitude")        
    
