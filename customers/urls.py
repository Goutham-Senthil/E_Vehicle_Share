# # customers/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
#     path('rent/', views.rent_vehicle, name='rent_vehicle'),
#     path('return/', views.return_vehicle, name='return_vehicle'), 
#     path('report/<int:reservation_id>/', views.report_vehicle, name='report_vehicle'),
#     path('payments/', views.payments, name='payments'),
#     path('make_payment/<int:transaction_id>/', views.make_payment, name='make_payment'),
#     path('add_funds/', views.add_funds, name='add_funds'),
#     path('transaction_history/', views.transaction_history, name='transaction_history'),
# ]
#previous above

# Imports
from django.urls import path
from . import views

# URL patterns for customer functionalities
urlpatterns = [
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),  # Customer dashboard
    path('rent/', views.rent_vehicle, name='rent_vehicle'),  # Rent a vehicle
    path('return/', views.return_vehicle, name='return_vehicle'),  # Return a rented vehicle
    path('report/<int:reservation_id>/', views.report_vehicle, name='report_vehicle'),  # Report an issue with a vehicle
    path('payments/', views.payments, name='payments'),  # View payment options
    path('make_payment/<int:transaction_id>/', views.make_payment, name='make_payment'),  # Make payment for a transaction
    path('add_funds/', views.add_funds, name='add_funds'),  # Add funds to account balance
    path('transaction_history/', views.transaction_history, name='transaction_history'),  # View transaction history
]
