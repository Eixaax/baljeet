"""mywallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from myweb import views
from django.conf import settings
from django.conf.urls.static import static
   
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
    path('home/',views.index,name='home'),
    path('logout/',views.logoutPage,name='logout'),
    path('about/',views.aboutPage,name='about'),
    path('delete/',views.deleterecord,name='del-record'),
    path('contact/',views.contactPage,name='contact'),
    path('search/', views.search_items, name='search_items'),
    path('addbal/', views.add_balance, name='add_balance'),
    path('dedbal/', views.deduct_balance, name='deduct_balance'),
    path('addsav/', views.add_savings, name='add_savings'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('additem/', views.add_items, name='add_items'),
    path('deleteitem/<item_id>',views.delete_items,name='delete-item'),
    path('updateitem/<item_id>', views.update_items, name='update-item'),
    path('addprofile/', views.add_profile, name='add_profile'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                