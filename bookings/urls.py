from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    # login / logout
    path('login/', auth_views.LoginView.as_view(template_name="bookings/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # registration
    path('register/', views.register, name='register'),

    # services
    path('services/', views.service_list, name='service_list'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),

    # bookings
    path('booking/<int:booking_id>/success/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
