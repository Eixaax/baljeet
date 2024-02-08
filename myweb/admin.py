from django.contrib import admin
from .models import Balance,Item,HistoryBalance,Feedback
# Register your models here.
admin.site.register(Balance),
admin.site.register(Item),
admin.site.register(HistoryBalance),
admin.site.register(Feedback),
