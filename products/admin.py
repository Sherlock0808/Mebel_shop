from django.contrib import admin
from .models import Products, ProductImage, FavouriteProducts, Categories, Basket, ProductColor, Subcategory

admin.site.register(Products)
admin.site.register(ProductImage)
admin.site.register(FavouriteProducts)
admin.site.register(Categories)
admin.site.register(Basket)
admin.site.register(ProductColor)
admin.site.register(Subcategory)
