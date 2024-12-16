from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return  self.name
class Product(models.Model):
    name = models.CharField(max_length=150, default='Product Name')
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    create_date = models.DateTimeField(auto_now_add=True)
    write_time = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='products')


    def __str__(self):
        return  self.name