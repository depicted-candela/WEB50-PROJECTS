from django.contrib import admin
from .models import User, Category, Auction, Bid, Comment

# Register your models here.

#class FlightCategory(admin.ModelAdmin):
#    list_display = ("__s_")

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)