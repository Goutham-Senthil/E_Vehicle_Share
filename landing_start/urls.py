# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.landing_page, name='landing_page'),
#     path('login/', views.login_page, name='login'),
#     path('register/', views.register, name='register'),
#     path('logout/', views.logout_user, name='logout'),
#     path('about_us/', views.about_us, name='about_us'),
#     path('contact/', views.contact, name='contact'),

# ]
# previous code above

# Imports
from django.urls import path
from . import views

# URL patterns for landing functionalities
urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Landing page
    path('login/', views.login_page, name='login'),  # Login page
    path('register/', views.register, name='register'),  # User registration page
    path('logout/', views.logout_user, name='logout'),  # Logout functionality
    path('about_us/', views.about_us, name='about_us'),  # About us page
    path('contact/', views.contact, name='contact'),  # Contact page
]
