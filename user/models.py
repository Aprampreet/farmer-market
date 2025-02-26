from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=6, null=True)
    phone = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=80, null=True)
    city = models.CharField(max_length=80, null=True)
    profile_image = models.ImageField(default='default.png', upload_to='profile_pics')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}-profile'
    

class BecomeFarmer(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)  # Changed from 'name' to 'farmer'
    company_name = models.CharField(max_length=200)
    total_land = models.FloatField()
    land_unit = models.CharField(max_length=20, choices=[('acre', 'Acre'), ('hectare', 'Hectare')])
    location_of_farm = models.CharField(max_length=700)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True) 
    state = models.CharField(max_length=100, blank=True, null=True) 
    addhar_image = models.ImageField(upload_to='farmer_addhar', null=True)
    become_farmer_vendor = models.BooleanField(default=False)  # ✅ Determines if the farmer is approved

    def __str__(self):
        return f"{self.farmer.username} - {self.company_name} Farming"



class FarmEquipmentImage(models.Model):
    farmer = models.ForeignKey(BecomeFarmer, on_delete=models.CASCADE, related_name="equipment_images")
    image = models.ImageField(upload_to="farm_equipment/")

    def __str__(self):
        return f"Equipment Image for Farmer ID {self.farmer.id}"
