from django.contrib import admin
from .models import User, Product, Order, OrderDetail, RatingReview, Transaction, SupportTicket

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(RatingReview)
admin.site.register(Transaction)
admin.site.register(SupportTicket)
