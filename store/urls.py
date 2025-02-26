from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('generate_qr/<int:product_id>/', views.generate_qr, name='generate_qr'),
    path('product/<int:product_id>/details', views.product_farm_detail, name='product_farm_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path("order-success/", views.order_success, name="order_success"),
    path('order-history/', views.order_history, name='order_history'),
    path("add-product/", views.add_product, name="add_product"),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('wishlist/',views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('nearby-products/', views.nearby_farmers_products, name='nearby_farmers_products'),
    path("farmer-orders/", views.farmer_orders, name="farmer_orders"),
    path("generate-order-qr/<int:order_id>/", views.generate_order_qr, name="generate_order_qr"),
    path("order-detail/<int:order_id>/", views.order_detail, name="order_detail"),  # ✅ FIXED!




]
