from django.shortcuts import get_object_or_404, render
from django.db import transaction

from django.http import JsonResponse
from .models import Product, Order, SupportTicket, Transaction, User, OrderDetail, RatingReview
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import viewsets
from .serializers import (UserSerializer, ProductSerializer, OrderSerializer, 
                          OrderDetailSerializer, RatingReviewSerializer, 
                          TransactionSerializer, SupportTicketSerializer)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# define ViewSets for DRF
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

class RatingReviewViewSet(viewsets.ModelViewSet):
    queryset = RatingReview.objects.all()
    serializer_class = RatingReviewSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer

# Customer-Side Views

# Product Browsing
@csrf_exempt
@require_http_methods(["GET"])
def product_search(request):
    search_query = request.GET.get('search', '')
    print("Search Query Received:", search_query)
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
        print("Filtered Products:", list(products.values('name')))
    else:
        products = Product.objects.all()
        print("All Products")

    products = products.values('id', 'name', 'price', 'description', 'category', 'image_url', 'stock_quantity', 'sales', 'is_featured')
    return JsonResponse(list(products), safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def product_detail(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        reviews = RatingReview.objects.filter(product=product)
        reviews_serializer = RatingReviewSerializer(reviews, many=True)

        product_details = {
            "name": product.name,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "image_url": product.image_url,
            "stock_quantity": product.stock_quantity,
            "sales": product.sales,
            "discount": product.discount,
            "reviews": reviews_serializer.data,  # Use serialized data with usernames
        }
        return JsonResponse(product_details)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found.'}, status=404)

# User Registration and Login
@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    data = json.loads(request.body)
    user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'], role='customer')
    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
    user.set_password(data['password'])
    user.save()
    return JsonResponse({'message': 'User registered successfully.'}, status=201)

@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({'message': 'Login successful', 'role': user.role}, status=200)
    else:
        print("Authentication failed")
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

from django.db.models import F  # Import F to perform field operations

# Place Order
@csrf_exempt
@login_required
def place_order(request):
    if request.user.role != 'customer':
        return JsonResponse({'error': 'Only customers can place orders.'}, status=403)
    
    try:
        data = json.loads(request.body)
        
        with transaction.atomic():  # Use a transaction to ensure data integrity
            # Create the order
            order = Order.objects.create(
                user=request.user,
                order_date=timezone.now(),
                status='Placed',
                total_price=data['total_price']
            )

            for item in data['items']:
                # Retrieve the product and update its stock and sales
                product = Product.objects.get(id=item['product_id'])
                
                # Create an order detail
                OrderDetail.objects.create(
                    order=order, 
                    product=product, 
                    quantity=item['quantity'], 
                    price_at_purchase=product.price * product.discount
                )
                
                # Update product's stock_quantity and sales
                Product.objects.filter(id=item['product_id']).update(
                    stock_quantity=F('stock_quantity') - item['quantity'],
                    sales=F('sales') + item['quantity']
                )
            
            # Create a transaction for this order
            Transaction.objects.create(
                order=order,
                transaction_date=timezone.now(),
                amount=order.total_price,
                payment_method="Credit",
                status="Success"
            )
            
            return JsonResponse({'message': 'Order and transaction recorded successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
# View Orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_orders(request):
    if request.user.is_authenticated and request.user.role == 'customer':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Authentication required.'}, status=401)

# Submitting Ratings and Reviews
@csrf_exempt
@require_http_methods(["POST"])
def submit_review(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=401)
    # Verify the user has purchased the product before allowing a review
    if not OrderDetail.objects.filter(order__user=request.user, product_id=product_id).exists():
        return JsonResponse({'error': 'Only customers who purchased the product can submit a review.'}, status=403)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=401)
    data = json.loads(request.body)
    product = get_object_or_404(Product, pk=product_id)
    review = RatingReview(product=product, user=request.user, rating=data['rating'], comment=data['comment'], review_date=data.get('review_date'))
    review.save()
    return JsonResponse({'message': 'Review submitted successfully.'})

#Submitting Support Tickets
@csrf_exempt
@require_http_methods(["POST"])
def submit_ticket(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=401)
    data = json.loads(request.body)
    ticket = SupportTicket(user=request.user, subject=data['subject'], description=data['description'])
    ticket.save()
    return JsonResponse({'message': 'Support ticket submitted successfully.'})

@csrf_exempt
@require_http_methods(["GET"])
def view_tickets(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=401)
    # Filter tickets by the logged-in user
    tickets = SupportTicket.objects.filter(user=request.user).order_by('creation_date').values()
    return JsonResponse(list(tickets), safe=False)


# Admin-side Views

# Product Management
@csrf_exempt
@require_http_methods(["POST"])
def add_product(request):
    if request.user.is_authenticated and request.user.role == 'admin':
        data = json.loads(request.body)
        product = Product(name=data['name'], category=data['category'], description=data['description'], image_url=data['image_url'], price=data['price'], discount=data['discount'], stock_quantity=data['stock_quantity'], is_featured=data['is_featured'])
        product.save()
        return JsonResponse({'message': 'Product added successfully.'})
    return JsonResponse({'error': 'Admin authentication required.'}, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def update_product(request, product_id):
    if not (request.user.is_authenticated and request.user.role == 'admin'):
        return JsonResponse({'error': 'Admin authentication required.'}, status=401)
    
    data = json.loads(request.body)
    try:
        product = Product.objects.get(id=product_id)
        # Update product fields
        for field, value in data.items():
            setattr(product, field, value)
        product.save()
        return JsonResponse({'message': 'Product updated successfully.'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found.'}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def delete_product(request, product_id):
    if not (request.user.is_authenticated and request.user.role == 'admin'):
        return JsonResponse({'error': 'Admin authentication required.'}, status=401)
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully.'})
    except Product.DoesNotExist:
        print("bad")
        return JsonResponse({'error': 'Product not found.'}, status=404)

# Transaction Management
@require_http_methods(["GET"])
def view_transaction(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return JsonResponse({'error': 'Admin privileges required.'}, status=403)
    transactions = Transaction.objects.all().values()
    return JsonResponse(list(transactions), safe=False)
    
# Managing Orders
@csrf_exempt
@require_http_methods(["POST"])
def update_orderstatus(request, order_id):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return JsonResponse({'error': 'Admin privileges required.'}, status=403)
    data = json.loads(request.body)
    order = get_object_or_404(Order, pk=order_id)
    order.status = data['status']
    order.save()
    return JsonResponse({'message': 'Order status updated successfully.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_view_orderdetials(request, order_id):
    if request.user.is_authenticated and request.user.role == 'admin':
        orderdetials = OrderDetail.objects.filter(order=order_id)
        serializer = OrderDetailSerializer(orderdetials, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Authentication required.'}, status=401)

# Managing Support Tickets
@csrf_exempt
@require_http_methods(["GET"])
def admin_view_tickets(request):
    if not (request.user.is_authenticated and request.user.role == 'admin'):
        return JsonResponse({'error': 'Authentication required.'}, status=401)
    
    tickets = SupportTicket.objects.order_by('creation_date').select_related('user').values(
        'id', 'subject', 'description', 'status', 'creation_date', 'resolution_date', 'user__username'
    )
    return JsonResponse(list(tickets), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def update_ticket(request, ticket_id):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return JsonResponse({'error': 'Admin privileges required.'}, status=403)
    data = json.loads(request.body)
    ticket = get_object_or_404(SupportTicket, pk=ticket_id)
    ticket.status = data['status']
    ticket.save()
    return JsonResponse({'message': 'Support ticket updated successfully.'})

