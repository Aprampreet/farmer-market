from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile ,BecomeFarmer, FarmEquipmentImage

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mt-1 mb-1'}),
            'email': forms.TextInput(attrs={'class': 'form-control mt-1 mb-1' }),
        }
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None   


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address','pincode','city','state', 'profile_image','latitude','longitude']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control mt-1 mb-1'}),
            'address': forms.TextInput(attrs={'class': 'form-control mt-1 mb-1'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control mt-1 mb-1'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control mt-1 mb-1'}),
            'city': forms.TextInput(attrs={'class': 'form-control mt-1 mb-1'}),
            'state': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'id': 'latitude', 'readonly': 'readonly'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'id': 'longitude', 'readonly': 'readonly'}),
        }



class BecomeFarmerForm(forms.ModelForm):
    class Meta:
        model = BecomeFarmer
        fields = ['company_name', 'total_land','pincode','city', 'land_unit','state', 'location_of_farm', 'addhar_image']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control mt-1 mb-1','placeholder' : 'Enter Company Name'}),
            'total_land': forms.NumberInput(attrs={'class': 'form-control mt-1 mb-1','placeholder' : 'Total Land Ownership'}),  
            'land_unit': forms.Select(attrs={'class': 'form-control mt-1 mb-1',}),
            'location_of_farm': forms.TextInput(attrs={'class': 'form-control mt-1 mb-1','placeholder' : 'Enter Farm Location'}),
            'addhar_image': forms.ClearableFileInput(attrs={'class': 'form-control mt-1 mb-1',}),
            'pincode':forms.TextInput(attrs={'class':'form-control mt-1 mb-1','placeholder':'Enter Pincode'}),
            'city':forms.TextInput(attrs={'class':'form-control mt-1 mb-1','placeholder':'Enter City'}),
            'state':forms.TextInput(attrs={'class':'form-control mt-1 mb-1','placeholder':'Enter State'}),

        }

class FarmEquipmentImageForm(forms.ModelForm):
    class Meta:
        model = FarmEquipmentImage
        fields = ['image']  # Remove widget modification here


