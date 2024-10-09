from django.shortcuts import render, HttpResponseRedirect
from .models import Products, Basket, FavouriteProducts, Subcategory, Categories, ProductImage
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import MessageForm
from django.contrib import messages as django_messages


def index(request, sub_id=None):
    if sub_id:
        category_list = Categories.objects.filter(sub_category=sub_id)
        product = []
        for category in category_list:
            product_list = Products.objects.filter(category=category)
            for i in product_list:
                if i != None:
                    product.append(i)
    else:
        product = Products.objects.all()
    subcategories = Subcategory.objects.all()
    sub_1 = subcategories[0:4]
    sub_2 = subcategories[4:7]
    sub_3 = subcategories[6]
    context = {
        'title': 'Store',
        'products': product,
        'subcategories': subcategories,
        'sub_1': sub_1,
        'sub_2': sub_2,
        'sub_3': sub_3,
    }
    return render(request, 'index_test.html', context)


@login_required
def basket(request):
    product = Products.objects.all()[:4]
    basket_products = Basket.objects.filter(user=request.user)
    total_quantity = Basket.objects.filter(user=request.user).total_quantity()
    total_price = Basket.objects.filter(user=request.user).total_sum()
    subcategories = Subcategory.objects.all()
    sub_1 = subcategories[0:4]
    sub_2 = subcategories[4:7]
    sub_3 = subcategories[6]
    context = {
        'title': 'Store',
        'products_box': basket_products,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'product_list': product,
        'subcategories': subcategories,
        'sub_1': sub_1,
        'sub_2': sub_2,
        'sub_3': sub_3,
    }
    return render(request, 'basket1.html', context)


@login_required
def basket_add(request, product_id):
    product = Products.objects.get(id=product_id)
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
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def favourites(request):
    favorites_product = FavouriteProducts.objects.filter(user=request.user)
    subcategories = Subcategory.objects.all()
    sub_1 = subcategories[0:4]
    sub_2 = subcategories[4:7]
    sub_3 = subcategories[6]
    context = {
        'title': 'Store',
        'products': favorites_product,
        'subcategories': subcategories,
        'sub_1': sub_1,
        'sub_2': sub_2,
        'sub_3': sub_3,
    }
    return render(request, 'favorites_products.html', context)


@login_required
def add_favourite(request, product_id):
    product = Products.objects.get(id=product_id)
    favourite, created = FavouriteProducts.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'Продукт {product.product_name} добавлен в избранное!')
    else:
        messages.info(request, f'Продукт {product.product_name} уже находится в избранном!')
    return HttpResponseRedirect(reverse('products:index'))

@login_required
def delete_favourite(request, product_id):
    product = FavouriteProducts.objects.get(id=product_id)
    product.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def product_search(request):
    query = request.GET.get('q')
    if query:
        products = Products.objects.filter(product_name__icontains=query)
    else:
        products = Products.objects.all()

    return render(request, 'index_test.html', {'products': products, 'query': query})


def product_info(request, product_id):
    product_box = Products.objects.all()
    main_product = Products.objects.filter(id=product_id)[0]
    product_main_picture = ProductImage.objects.filter(product=product_id)[0]
    product_pictures = ProductImage.objects.filter(product=product_id)[1:]
    subcategories = Subcategory.objects.all()
    sub_1 = subcategories[0:4]
    sub_2 = subcategories[4:7]
    sub_3 = subcategories[6]
    context = {
        'title': 'Product',
        'products': product_box,
        'main_product': main_product,
        'photos': product_pictures,
        'main_photo': product_main_picture,
        'subcategories': subcategories,
        'sub_1': sub_1,
        'sub_2': sub_2,
        'sub_3': sub_3,
    }
    return render(request, 'product_info.html', context)


def about(request):
    subcategories = Subcategory.objects.all()
    sub_1 = subcategories[0:4]
    sub_2 = subcategories[4:7]
    sub_3 = subcategories[6]
    context = {
        'title': 'About',
        'subcategories': subcategories,
        'sub_1': sub_1,
        'sub_2': sub_2,
        'sub_3': sub_3,
    }
    return render(request, 'about_us.html', context)


def contact(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Ваше сообщение было успешно отправлено!')
            return HttpResponseRedirect(reverse('products:index'))
        else:
            django_messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = MessageForm()
    subcategories = Subcategory.objects.all()
    sub_1 = subcategories[0:4]
    sub_2 = subcategories[4:7]
    sub_3 = subcategories[6]
    context = {
        'title': 'Contacts',
        'subcategories': subcategories,
        'sub_1': sub_1,
        'sub_2': sub_2,
        'sub_3': sub_3,
        'form': form
    }
    return render(request, 'contacts.html', context)

