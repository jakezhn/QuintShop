from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, ProductViewSet, OrderViewSet, OrderDetailViewSet,
                    RatingReviewViewSet, TransactionViewSet, SupportTicketViewSet)
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order_details', OrderDetailViewSet)
router.register(r'ratings_reviews', RatingReviewViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'support_tickets', SupportTicketViewSet)

urlpatterns = [
    # Customer side APIs
    path('', include(router.urls)),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.user_login, name='user_login'),

    path('product_search/', views.product_search, name='product_search'),

    path('place_order/', views.place_order, name='place_order'),
    path('my_orders/', views.view_orders, name='view_orders'),

    path('products/<int:product_id>/submit_review/', views.submit_review, name='submit_review'),
    path('products/<int:pk>/product_detail/', views.product_detail, name='product_detail'),

    path('my_tickets/', views.view_tickets, name='view_tickets'),
    path('my_tickets/submit_ticket/', views.submit_ticket, name='submit_ticket'),

    # Admin side APIs
    path('admin/products/add_product/', views.add_product, name='add_product'),
    path('admin/products/<int:product_id>/update_product/', views.update_product, name='update_product'),
    path('admin/products/<int:product_id>/delete_product/', views.delete_product, name='delete_product'),

    path('admin/transactions/view_transaction/', views.view_transaction, name='view_transaction'),

    path('admin/orders/<int:order_id>/update_orderstatus/', views.update_orderstatus, name='update_orderstatus'),
    path('admin/orders/<int:order_id>/admin_view_orderdetials/', views.admin_view_orderdetials, name='admin_view_orderdetials'),

    path('admin/support_tickets/<int:ticket_id>/update_ticket/', views.update_ticket, name='update_ticket'),
    path('admin/support_tickets/', views.admin_view_tickets, name='admin_view_tickets'),
]