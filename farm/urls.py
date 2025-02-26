"""
URL configuration for farm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_view


urlpatterns = [
    path('admin/', admin.site.urls , name='admin'),
    path('',include('store.urls')),
    path('login/',user_view.login_view,name='login'),
    path('register/',user_view.register_view,name='register'),
    path('logout/',user_view.logout_view,name='logout'),
    path('profile/',user_view.profile,name='profile'),
    path('profile-update/',user_view.profile_update,name='profile_update'),
    path('become-farmer/', user_view.become_farmer_view, name='become_farmer'),
    path('admin-panel/farmer-requests/', user_view.admin_farmer_requests, name='admin_farmer_requests'),
    path('admin-panel/approve-farmer/<int:farmer_id>/', user_view.approve_farmer, name='approve_farmer'),
    path('admin-panel/reject-farmer/<int:farmer_id>/', user_view.reject_farmer, name='reject_farmer'),

]
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
