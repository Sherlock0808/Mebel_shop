from django.contrib import admin
from .models import Categories, Subcategory, Product, ProductImage, ProductColor, Basket, FavouriteProduct, Messages

admin.site.register(Categories)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductColor)
admin.site.register(Basket)
admin.site.register(FavouriteProduct)
admin.site.register(Messages)
