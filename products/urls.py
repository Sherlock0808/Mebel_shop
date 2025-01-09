from django.urls import path
from .views import (index, about, contact, favourites, add_favourite, delete_favourite, basket, basket_add,
                    basket_remove,
                    product_search, product_info, create_payment_intent, payment_page, payment_success)

urlpatterns = [
    path('', index, name='index'),
    path('filter/<int:category_id>/', index, name='filter'),
    path('about_us/', about, name='about'),
    path('contact_us/', contact, name='contact'),
    path('favorites/', favourites, name='favorites_products'),
    path('favorites/add/<int:product_id>/', add_favourite, name='add_favourite'),
    path('favorites/remove/<int:product_id>/', delete_favourite, name='delete_favourite'),
    path('basket/', basket, name='basket'),
    path('basket/add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('search/', product_search, name='product_search'),
    path('product/<int:product_id>/', product_info, name='product_info'),
    path("create-payment-intent/", create_payment_intent, name="create_payment_intent"),
    path("payment/", payment_page, name="payment_page"),
    path("payment-success/", payment_success, name="payment_success"),
]
