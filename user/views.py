from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.models import User
# Create your views here.



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if len(password1) >= 6:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists. Please choose a different username.')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user
                    user.save()
                    return redirect('login') 
            else:
                messages.error(request, 'Passwords length must be of 6 digits.')
        else:
            messages.error(request, 'Passwords doesnot match.')
    return render(request,'user/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            Profile.objects.get_or_create(user=user)

            return redirect('profile_update')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'user/login.html')



@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.warning(request,'You Have Been Logged Out. Sign In Again. ')
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    return render(request,'user/profile.html')

@login_required(login_url='login')
def profile_update(request):
    # Ensure user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user/profile_update.html', context)



@login_required(login_url='login')
def become_farmer_view(request):
    farmer_instance = BecomeFarmer.objects.filter(farmer=request.user).first()
    
    if farmer_instance:
        messages.info(request, "You have already submitted a request or are a farmer.")
        return redirect('home')

    if request.method == "POST":
        farmer_form = BecomeFarmerForm(request.POST, request.FILES)
         
        if farmer_form.is_valid():
            farmer = farmer_form.save(commit=False)
            farmer.farmer = request.user  # ✅ FIX: Assign farmer correctly
            farmer.become_farmer_vendor = False  
            farmer.save()

            # ✅ Saving multiple equipment images (if any)
            images = request.FILES.getlist('images')  
            for img in images:
                FarmEquipmentImage.objects.create(farmer=farmer, image=img)

            messages.success(request, "Your request has been submitted for approval.")
            return redirect('home')  

    else:
        farmer_form = BecomeFarmerForm()

    return render(request, 'user/become_farmer.html', {'farmer_form': farmer_form})



@login_required(login_url='login')
def admin_farmer_requests(request):
    if not request.user.is_superuser:
        return redirect('home')

    farmers = BecomeFarmer.objects.filter(become_farmer_vendor=False)
    return render(request, 'admin/farmer_requests.html', {'farmers': farmers})

@login_required(login_url='login')
def approve_farmer(request, farmer_id):
    if not request.user.is_superuser:
        return redirect('home')

    farmer = BecomeFarmer.objects.get(id=farmer_id)
    farmer.become_farmer_vendor = True  # Mark as an approved farmer
    farmer.save()
    
    messages.success(request, f"{farmer.farmer.username} has been approved as a farmer.")
    return redirect('admin_farmer_requests')

@login_required(login_url='login')
def reject_farmer(request, farmer_id):
    if not request.user.is_superuser:
        return redirect('home')

    farmer = BecomeFarmer.objects.get(id=farmer_id)
    farmer.delete()  # Remove rejected requests

    messages.warning(request, "Farmer request rejected.")
    return redirect('admin_farmer_requests')
