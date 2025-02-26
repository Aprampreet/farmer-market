from django.db import models
from django.contrib.auth.models import User



class Products(models.Model):
    CATEGORY_CHOICES = [
        ('organic', 'Organic'),
        ('semi_organic', 'Semi-Organic'),
        ('chemical', 'Chemical'),
    ]
    TYPE_CHOICES = [
        ('fruits', 'Fruits'),
        ('vegetables', 'Vegetables'),
        ('dry-fruits', 'Dry-Fruits'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='organic')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='vegetables')
    name = models.CharField(max_length=300)
    small_discription = models.CharField(max_length=200)
    discription = models.TextField()
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_pics', null=True, blank=True)  # ✅ Fix: Allow blank images
    farming_video = models.FileField(upload_to='products_videos/', null=True, blank=True)  # ✅ Fix: Allow blank videos
    origen_of_farming = models.CharField(max_length=250)
    origen_details = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def get_discount_amount(self):
        return (self.product.mrp - self.product.selling_price) * self.quantity if self.product.mrp > self.product.selling_price else 0

    def get_final_price(self):
        return self.product.selling_price * self.quantity

    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=700)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Products, through='OrderItem')  
    status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('shipped', 'Shipped'),
            ('out_for_delivery', 'Out for Delivery'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ], 
        default='pending'
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user.username if self.user else 'Unknown'}"

    def get_farmer_products(self, farmer):
        """Returns products from this order that belong to a specific farmer."""
        return self.items.filter(farmer=farmer)



    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name} ({self.quantity})"


    
class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)  
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='review_images/', null=True, blank=True) 


    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"


class Wishlist (models.Model):
    product = models.ForeignKey(Products ,on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} added {self.product.name} to wishlist' 