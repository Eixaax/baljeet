from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
                     
class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)    
    profile_picture = models.ImageField(null=True, blank=True,upload_to='images/')
    
    def __str__(self):
        return self.user.username
    
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    price = models.IntegerField()
    price2 = models.IntegerField()
    desc= models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

 
    def __str__(self):
        return f'{self.name} : {self.user.username}'
    
class HistoryBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_added = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    amount_history = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    type = models.CharField(max_length=80)    
    date = models.DateField(default=timezone.now) 
    def __str__(self):
        return self.user.username
    
class Feedback(models.Model):
    fullname = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    message = models.TextField(max_length=200)
    
    def __str__(self):
        return self.fullname