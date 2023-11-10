from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128, verbose_name='password')
    password_2 = models.CharField(max_length=128, verbose_name="password_2")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = []


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Categories(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, related_name="subcategories")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-price"]


class BaseItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CartItem(BaseItem):
    quantity = models.PositiveIntegerField(default=1)
    pass

    class Meta:
        verbose_name = "Товар корзины пользователя"
        verbose_name_plural = "Товары корзины пользователей"

    def __str__(self):
        return f"{self.product.name} - {self.product.category.name}"


class WishListItem(BaseItem):
    pass

    class Meta:
        verbose_name = "Желаемый товар пользователя"
        verbose_name_plural = "Желаемые товары пользователей"


class Order(models.Model):
    STATUS_CHOICES = [
        ("successful", "Successful"),
        ("canceled", "Canceled"),
        ("in_transit", "In transit"),
        ("delivered", "Delivered")
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart =
    creation_date = models.DateTimeField(auto_now=True)
    overall = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Successful")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

# models.ManyToManyField(CartItem, choices=)
