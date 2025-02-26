from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import *
import qrcode
from user.models import *
from io import BytesIO
from django.http import HttpResponse
from .forms import ProductForm  ,ReviewForm
from django.urls import reverse
from geopy.distance import geodesic
from django.db.models import Avg
from django.contrib import messages
from .models import Products
from user.models import BecomeFarmer 
from .forms import ProductForm

# Create your views here.
def home(request):
    products = Products.objects.all().order_by('-id')
    category = request.GET.get('category') 
    selected_type = request.GET.get('type')
    search_query = request.GET.get('search', '')

    if request.user.is_authenticated:
        user_profile = Profile.objects.filter(user = request.user ).first()

        

    if category:
        products = products.filter(category=category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    for product in products:
        reviews = product.reviews.all()
        total_rating = sum(review.rating for review in reviews)  
        total_reviews = len(reviews)  

        if total_reviews > 0:
            product.average_rating = total_rating / total_reviews  
            product.average_rating = round(product.average_rating, 1)
        
        else:
            product.average_rating = 0 

    context= {
        'products':products,
        'selected_category': category, 
        'selected_type': selected_type,
        'search_query': search_query,

    }
    return render(request,'store/home.html',context)



def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    reviews = product.reviews.all().order_by('-created_at')  
    total_rating = sum(review.rating for review in reviews)
    total_reviews = len(reviews)

    # Calculate the average rating
    average_rating = round(total_rating / total_reviews, 1) if total_reviews > 0 else 0  

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted successfully! ✅")
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, "Error submitting the review. Please check your inputs. ❌")

    else:
        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating,
    }
   
    return render(request, 'store/product_detail.html', context)




@login_required(login_url='/login/')
def delete_review(request, review_id):
    review = get_object_or_404(Reviews, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Your review has been deleted successfully! ✅")
        return redirect('product_detail', product_id=review.product.id)

    messages.error(request, "Failed to delete the review. Please try again. ❌")
    return redirect('product_detail', product_id=review.product.id)



@login_required(login_url='/login/')
def generate_qr(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    product_url = request.build_absolute_uri(reverse('product_farm_detail', args=[product.id]))  

    qr = qrcode.make(product_url)  
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")



def product_farm_detail(request,product_id):
    product = get_object_or_404(Products, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'store/product_farm_detail.html', context)


@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')



@login_required(login_url='/login/')
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-id')

    total_price = sum(item.get_final_price() for item in cart_items)
    total_discount = sum(item.get_discount_amount() for item in cart_items)
    final_price = total_price - total_discount  # Final price after discounts

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_discount': total_discount,
        'final_price': final_price
    }
    return render(request, 'store/cart.html', context)



@login_required(login_url='/login/')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required(login_url='/login/')
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required(login_url='/login/')
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  

    return redirect('view_cart')


@login_required(login_url='/login/')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("view_cart")

    total_price = sum(item.get_final_price() for item in cart_items)
    total_discount = sum((item.product.mrp - item.product.selling_price) * item.quantity for item in cart_items)
    shipping_cost = 50  
    final_total = total_price - total_discount + shipping_cost

    if request.method == "POST":
        full_name = request.POST["full_name"]
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        zip_code = request.POST["zip_code"]
        phone = request.POST["phone"]

        # ✅ Check stock availability for all cart items
        for item in cart_items:
            product = item.product
            if item.quantity > product.quantity:
                messages.error(request, f"Not enough stock for {product.name}. Available: {product.quantity}")
                return redirect("view_cart")  # Redirect back to cart

        # ✅ Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            total_price=final_total
        )

        # ✅ Loop through cart items to create OrderItems and update stock
        for item in cart_items:
            product = item.product

            # ✅ Reduce product quantity
            product.quantity -= item.quantity
            product.save()

            # ✅ Create OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.selling_price
            )

            # ✅ Delete the product if quantity becomes 0
            if product.quantity == 0:
                product.delete()

        # ✅ Empty the cart after successful order placement
        cart_items.delete()
        messages.success(request, "Order placed successfully!")

        return redirect("order_success")

    return render(request, "store/checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "total_discount": total_discount,
        "shipping_cost": shipping_cost,
        "final_total": final_total,
    })



@login_required(login_url='/login/')
def order_success(request):
    return render(request, "store/order_success.html")

@login_required(login_url='/login/')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order.html', {'orders': orders})




@login_required(login_url='/login/')
def add_product(request):
    farmer_profile = BecomeFarmer.objects.filter(farmer=request.user, become_farmer_vendor=True).first()
    
    if not farmer_profile:
        messages.error(request, "You must be an approved farmer to add products.")
        return redirect('home')
    
    if request.method == 'POST':
        
        form = ProductForm(request.POST, request.FILES)  
        print(farmer_profile.farmer)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user  
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('home')  
        else:
            messages.error(request, "Error adding product. Please check your inputs.")

    else:
        form = ProductForm()

    return render(request, "store/add_product.html", {"form": form})
 





@login_required(login_url='/login/')
def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id, farmer=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, "Error updating product. Please check your inputs.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/edit_product.html', {'form': form})




@login_required(login_url='/login/')
def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id, farmer=request.user)

    if request.method == "POST":
        product.delete()
        return redirect('home')  
    return render(request, 'store/delete_product.html', {'product': product})




@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, f"Added {product.name} to your wishlist! ❤️")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")

    return redirect('wishlist')


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)

    for item in wishlist_items:
        reviews = item.product.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        total_reviews = len(reviews)

        if total_reviews > 0:
            item.product.average_rating = round(total_rating / total_reviews, 1)
        else:
            item.product.average_rating = 0

    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})



@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)

    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request, f"Removed {product.name} from your wishlist. ❌")
    else:
        messages.warning(request, f"{product.name} is not in your wishlist.")

    return redirect('wishlist')






@login_required
def nearby_farmers_products(request):
    user_profile = Profile.objects.get(user=request.user)

    if not user_profile.latitude or not user_profile.longitude:
        return render(request, 'store/nearby_farmers_products.html', {'products': [], 'error': 'Please update your location in profile settings.'})

    user_location = (user_profile.latitude, user_profile.longitude)

    nearby_farmers = []
    all_farmers = Profile.objects.exclude(latitude=None).exclude(longitude=None)

    for farmer in all_farmers:
        farmer_location = (farmer.latitude, farmer.longitude)
        distance = geodesic(user_location, farmer_location).km  

        if distance <= 50:
            nearby_farmers.append(farmer)

    farmer_users = [farmer.user for farmer in nearby_farmers]  

    products = Products.objects.filter(farmer__in=farmer_users).annotate(average_rating=Avg('reviews__rating')).order_by('-average_rating')

    # ✅ Round off ratings for better display
    for product in products:
        product.average_rating = round(product.average_rating or 0, 1)

    return render(request, 'store/nearby_farmers_products.html', {'products': products})






from django.http import JsonResponse

def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': order.status})

    return render(request, 'store/track_order.html', {'order': order})


@login_required
def farmer_orders(request):
    farmer = request.user

    # Get all orders that contain products from this farmer
    orders = Order.objects.filter(items__farmer=farmer).distinct()

    # Include only farmer's products in each order
    for order in orders:
        order.farmer_products = OrderItem.objects.filter(order=order, product__farmer=farmer)

    return render(request, 'store/farmer_orders.html', {'orders': orders})









@login_required
def generate_order_qr(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # ✅ Correct URL for order detail
    order_url = request.build_absolute_uri(reverse('order_detail', args=[order.id]))  

    qr = qrcode.make(order_url)  
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_detail.html', {'order': order})