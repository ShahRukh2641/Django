"""crm1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_view
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account'),
    path('customers/<str:pk>', views.customers, name='customer'),
    path('products/', views.products, name='product'),
    path('create_order/<str:pk>', views.createOrder, name='create_order'),
    path('update_order/<str:pk>', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>', views.deleteOrder, name='delete_order'),

    path('reset_password', auth_view.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/<uid64>/<token>', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
