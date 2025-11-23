# # operators/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboard/', views.operator_dashboard, name='operator_dashboard'),
#     path('move_vehicles/',views.move_vehicle, name='move_vehicle'),
#     path('track_vehicle/',views.track_vehicle, name='track_vehicle'),
#     path('repair/<int:vehicle_id>/', views.repair_vehicle, name='repair_vehicle'),
#     path('charge_record/', views.charge_record, name='charge_record'),
#     path('maintenance_record/', views.maintenance_record, name='maintenance_record'),
#     path('charge_vehicle/<int:vehicle_id>/', views.charge_vehicle,name='charge_vehicle')

# ]
#previous code above

# operators/urls.py

# Imports
from django.urls import path
from . import views

# URL patterns for operator functionalities
urlpatterns = [
    path('dashboard/', views.operator_dashboard, name='operator_dashboard'),  # Operator dashboard
    path('move_vehicles/', views.move_vehicle, name='move_vehicle'),  # Move vehicle to a new location
    path('track_vehicle/', views.track_vehicle, name='track_vehicle'),  # Track a specific vehicle
    path('repair/<int:vehicle_id>/', views.repair_vehicle, name='repair_vehicle'),  # Repair a specific vehicle
    path('charge_record/', views.charge_record, name='charge_record'),  # View charging records
    path('maintenance_record/', views.maintenance_record, name='maintenance_record'),  # View maintenance records
    path('charge_vehicle/<int:vehicle_id>/', views.charge_vehicle, name='charge_vehicle')  # Charge a specific vehicle
]
