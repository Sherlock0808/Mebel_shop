from django.db import models
from users.models import User
from PIL import Image
from io import BytesIO
from django.core.files import File

class Subcategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    icon = models.FileField(upload_to='icons', null=True, blank=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)
    recommended_place_of_using = models.CharField(max_length=50)
    sub_category = models.ManyToManyField(Subcategory)

    def __str__(self):
        return self.name


class Products(models.Model):
    product_name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    characteristic = models.TextField()
    length = models.CharField(max_length=20, default=0)
    width = models.CharField(max_length=20, default=0)
    height = models.CharField(max_length=20, default=0)
    main_foto = models.ImageField(upload_to='main_product_images', null=True, blank=True)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f'Продукт: {self.product_name} | Категория: {self.category.name}'


class ProductImage(models.Model):
    product = models.ForeignKey(Products, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    image_mini = models.ImageField(upload_to='mini_product_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.product.product_name} Image'

    def save(self, *args, **kwargs):
        # Сначала сохраняем основное изображение
        super().save(*args, **kwargs)

        # Открываем сохраненное изображение
        if self.image and not self.image_mini:
            img = Image.open(self.image)

            # Изменяем размер изображения до миниатюры (например, 200x200)
            img = img.resize((104, 42))

            # Сжимаем изображение и сохраняем его в формате JPEG
            img_io = BytesIO()
            img.save(img_io, format='PNG', quality=100)  # Сжатие с качеством 85%
            img_file = File(img_io, name=self.image.name)

            # Сохраняем сжатую версию изображения в поле image_mini
            self.image_mini.save(f"{self.image.name}", img_file, save=False)

        super().save(*args, **kwargs)


class ProductColor(models.Model):
    product = models.ForeignKey(Products, related_name='colors', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.product_name} Color - {self.color}"


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    product_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    length = models.CharField(max_length=20, default=0)
    width = models.CharField(max_length=20, default=0)
    height = models.CharField(max_length=20, default=0)
    main_foto = models.ImageField(upload_to='main_product_images', null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)


    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для: {self.user.username} | Продукт: {self.product.product_name}'

    def save(self, *args, **kwargs):
        self.product_name = self.product.product_name
        self.price = self.product.price
        self.length = self.product.length
        self.width = self.product.width
        self.height = self.product.height
        self.main_foto = self.product.main_foto

        super().save(*args, **kwargs)

    def sum(self):
        return self.product.price * self.quantity


class FavouriteProducts(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    product_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    length = models.CharField(max_length=20, default=0)
    width = models.CharField(max_length=20, default=0)
    height = models.CharField(max_length=20, default=0)
    main_foto = models.ImageField(upload_to='main_product_images', null=True, blank=True)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f'Избранный продукт - <{self.product.product_name}> для пользователя - {self.user.username}'

    def save(self, *args, **kwargs):
        self.product_name = self.product.product_name
        self.price = self.product.price
        self.length = self.product.length
        self.width = self.product.width
        self.height = self.product.height
        self.main_foto = self.product.main_foto
        self.category = self.product.category

        super().save(*args, **kwargs)


class Messages(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f'Сообщение от {self.name}'





