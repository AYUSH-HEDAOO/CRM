
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
  
urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('user/', views.userPage, name="userPage"),
    path('profile/', views.customerProfile, name='customerProfile'),
    path('logout/', views.logoutUser, name="logout"),  
    path('customer/<str:pk>/', views.customer, name="customer"),
]
if settings.DEBUG:  # This ensures media is served only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)