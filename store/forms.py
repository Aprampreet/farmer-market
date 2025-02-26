from .models import Products,Reviews
from django import forms



from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            "name",
            "category",
            "type",
            "small_discription",
            "discription",
            "mrp",
            "selling_price",
            "quantity",
            "image",
            "farming_video",
            "origen_of_farming",
            "origen_details",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter product name"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
            "small_discription": forms.TextInput(attrs={"class": "form-control", "placeholder": "Short description"}),
            "discription": forms.Textarea(attrs={"class": "form-control", "placeholder": "Detailed description", "rows": 4}),
            "mrp": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "selling_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),  # ✅ Fix: Accept only images
            "farming_video": forms.FileInput(attrs={"class": "form-control", "accept": "video/*"}),  # ✅ Fix: Accept only videos
            "origen_of_farming": forms.TextInput(attrs={"class": "form-control", "placeholder": "Origin of farming"}),
            "origen_details": forms.Textarea(attrs={"class": "form-control", "placeholder": "Details about the farm", "rows": 3}),
        }



class ReviewForm(forms.ModelForm):
    class Meta : 
        model = Reviews
        fields = ['rating', 'comment','image']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }