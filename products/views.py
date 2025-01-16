from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MessageForm
from .models import Product, Basket, FavouriteProduct, ProductImage, Categories, Subcategory

from .forms import PaymentForm
import stripe
from django.conf import settings
from django.http import JsonResponse


# Установка секретного ключа Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(request):
    """
    Создает PaymentIntent на общую сумму корзины.
    """
    try:
        # Рассчитайте общую сумму заказа
        basket_products = Basket.objects.filter(user=request.user)
        total_price = basket_products.total_sum()
        amount = int(total_price * 100)  # Переводим в центы

        # Создаем PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method_types=["card"],
        )
        return JsonResponse({"clientSecret": intent.client_secret})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def payment_page(request):
    """
    Отображает страницу оплаты с информацией о заказе.
    """
    basket_products = Basket.objects.filter(user=request.user)
    total_quantity = basket_products.total_quantity()
    total_price = int(basket_products.total_sum())

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Сохраняем данные пользователя и создаем PaymentIntent
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]

            try:
                # Перенаправляем на страницу успешной оплаты
                request.session["name"] = name
                request.session["email"] = email
                request.session["total_price"] = total_price
                return redirect("products:payment_success")
            except Exception as e:
                return render(request, "payment1.html", {
                    "cart_items": basket_products,
                    "total_quantity": total_quantity,
                    "total_price": total_price,
                    "form": form,
                    "error": str(e),
                    "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
                })
    else:
        form = PaymentForm()

    return render(request, "payment1.html", {
        "cart_items": basket_products,
        "total_quantity": total_quantity,
        "total_price": total_price,
        "form": form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    })


def payment_success(request):
    """
    Отображает страницу успешного платежа.
    """
    name = request.session.get("name", "Клиент")
    email = request.session.get("email", "не указан")
    total_price = request.session.get("total_price", 0)

    return render(request, "payment_success.html", {
        "name": name,
        "email": email,
        "total_price": total_price,
    })


def index(request, category_id=None):
    if category_id:
        category_list = Categories.objects.filter(sub_category=category_id)
        product = []
        for category in category_list:
            product_list = Product.objects.filter(category=category)
            for i in product_list:
                if i != None:
                    product.append(i)
    else:
        product = Product.objects.all()
    subcategories = Subcategory.objects.all()
    context = {
        'title': 'Store',
        'products': product,
        'subcategories': subcategories
    }
    return render(request, 'main_index.html', context)


def about(request):
    subcategories = Subcategory.objects.all()
    return render(request, 'about_us.html', {'subcategories': subcategories})


def contact(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение отправлено!')
            return HttpResponseRedirect(reverse('products:index'))
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме!')
    else:
        form = MessageForm()
    subcategories = Subcategory.objects.all()
    context = {
        'title': 'Contacts',
        'form': form,
        'subcategories': subcategories
    }
    return render(request, 'contacts.html', context)


@login_required
def favourites(request):
    favourites_product = FavouriteProduct.objects.filter(user=request.user)
    subcategories = Subcategory.objects.all()
    context = {
        'title': 'Favorites',
        'products': favourites_product,
        'subcategories': subcategories
    }
    return render(request, 'favorites_products.html', context)


@login_required
def add_favourite(request, product_id):
    product = Product.objects.get(id=product_id)
    favourite, created = FavouriteProduct.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'Продукт {product.product_name} добавлен в избранное!')
    else:
        messages.info(request, f'Продукт {product.product_name} уже находится в избранном!')
    return HttpResponseRedirect(reverse('products:index'))


@login_required
def delete_favourite(request, product_id):
    product = FavouriteProduct.objects.get(id=product_id)
    product.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket(request):
    product = Product.objects.all()[:4]
    basket_products = Basket.objects.filter(user=request.user)
    total_quantity = basket_products.total_quantity()
    total_price = basket_products.total_sum()
    subcategories = Subcategory.objects.all()
    context = {
        'title': 'Basket',
        'products_box': basket_products,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'product_list': product,
        'subcategories': subcategories
    }
    return render(request, 'basket1.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket_box = baskets.first()
        basket_box.quantity += 1
        basket_box.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket_obj = Basket.objects.get(id=basket_id)
    basket_obj.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def product_search(request):
    query = request.GET.get('q')
    if query:
        product = Product.objects.filter(product_name__icontains=query)
    else:
        product = Product.objects.all()
    return render(request, 'main_index.html', {'products':product, 'query':query})


def product_info(request, product_id):
    product_box = Product.objects.all()
    main_product = Product.objects.filter(id=product_id)[0]
    product_main_picture = ProductImage.objects.filter(product=product_id)[0]
    product_pictures = ProductImage.objects.filter(product=product_id)[1:]
    subcategories = Subcategory.objects.all()
    context = {
        'title': 'Product',
        'products': product_box,
        'main_product': main_product,
        'photos': product_pictures,
        'main_photo': product_main_picture,
        'subcategories': subcategories
    }
    return render(request, 'product_info.html', context)






