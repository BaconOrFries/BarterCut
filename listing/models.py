from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    item_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank= True, null=True)
    point = models.IntegerField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    listed_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    received_by = models.ForeignKey(User, related_name='received_items', on_delete=models.CASCADE, null=True, blank=True)
    listed_at = models.DateTimeField(auto_now_add=True)

    TRANSACTION_STATUS_CHOICES = [
        ('Listed', 'Listed'),
        ('Sold', 'Sold'),
    ]
    transaction_status = models.CharField(
        max_length=10,
        choices=TRANSACTION_STATUS_CHOICES,
        default='Listed',
    )

    def __str__(self):
        return self.name