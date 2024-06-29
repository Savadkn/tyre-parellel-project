from django.contrib import admin

# Register your models here.
from shop.models import Size,Category,Brand,Tag,Product

admin.site.register(Size)

admin.site.register(Category)

admin.site.register(Brand)

admin.site.register(Tag)

admin.site.register(Product)
