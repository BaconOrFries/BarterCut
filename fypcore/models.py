from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=20)

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transacation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')