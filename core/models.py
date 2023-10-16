from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128, verbose_name='password')
    password_2 = models.CharField(max_length=128, verbose_name="password_2")


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)


class Categories(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, related_name="subcategories")

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name