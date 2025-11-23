# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from customers.models import User, Vehicle, Reservation, Payment
# from django.utils import timezone
# import json
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from customers.models import Vehicle

# @login_required(login_url='login')
# def customer_dashboard(request):
#     user = request.user
#     reservations = Reservation.objects.filter(user=user)
#     payments = Payment.objects.filter(user=user)

#     context = {
#         'user': user,
#         'reservations': reservations,
#         'payments': payments
#     }

#     return render(request, 'customers/dashboard.html', context)

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from customers.models import User, Vehicle, Reservation, Payment
# from django.utils import timezone
# import json
# from django.contrib import messages  # Import for adding messages

# @login_required(login_url='login')
# def rent_vehicle(request):
#     vehicles = Vehicle.objects.filter(is_available=True)  # Only show available vehicles

#     # Convert vehicle data to JSON for rendering markers on the map
#     vehicles_list = [
#         {
#             "vehicle_id": vehicle.vehicle_id,
#             "vehicle_name": vehicle.vehicle_name,
#             "vehicle_type": vehicle.vehicle_type,
#             "battery": vehicle.battery,
#             "hourly_rate": vehicle.hourly_rate,
#             "latitude": vehicle.latitude,
#             "longitude": vehicle.longitude
#         }
#         for vehicle in vehicles
#     ]
#     vehicles_json = json.dumps(vehicles_list)

#     if request.method == "POST":
#         vehicle_id = request.POST.get("vehicle_id")
        
#         # Fetch the vehicle object
#         try:
#             vehicle = Vehicle.objects.get(pk=vehicle_id, is_available=True)
#         except Vehicle.DoesNotExist:
#             messages.error(request, "The selected vehicle is no longer available.")
#             return redirect('rent_vehicle')

#         # Create a new reservation
#         reservation = Reservation.objects.create(
#             vehicle=vehicle,
#             user=request.user,
#             start_time=timezone.now(),
#             status='In use'
#         )

#         # Mark the vehicle as not available
#         vehicle.is_available = False
#         vehicle.save()

#         messages.success(request, f"You have successfully rented {vehicle.vehicle_name}.")
#         return redirect('customer_dashboard')

#     context = {
#         "vehicles": vehicles,
#         "vehicles_json": vehicles_json
#     }

#     return render(request, 'customers/rent.html', context)



# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from customers.models import Vehicle, Reservation, Report
# from django.utils import timezone
# from django.contrib import messages

# # customers/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from customers.models import Reservation
# from django.utils import timezone
# from django.contrib import messages

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from customers.models import Reservation, Report, Payment
# from django.utils import timezone
# from django.contrib import messages

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from customers.models import Reservation, Report, Payment
# from django.utils import timezone
# from django.contrib import messages

# @login_required(login_url='login')
# def return_vehicle(request):
#     reservations = Reservation.objects.filter(user=request.user, status='In use')

#     if request.method == 'POST':
#         reservation_id = request.POST.get('reservation_id')
#         action_type = request.POST.get('action_type')
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')

#         try:
#             reservation = Reservation.objects.get(pk=reservation_id, user=request.user, status='In use')
#         except Reservation.DoesNotExist:
#             messages.error(request, "Reservation not found or vehicle is not in use.")
#             return redirect('return_vehicle')

#         if action_type == 'return':
#             # Update reservation and vehicle status
#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.vehicle.is_available = True

#             # Update vehicle location
#             if latitude and longitude:
#                 reservation.vehicle.latitude = latitude
#                 reservation.vehicle.longitude = longitude

#             reservation.vehicle.save()
#             reservation.save()

#             # Calculate payment based on rental duration and hourly rate
#             battery = reservation.vehicle.battery
#             rental_duration = (reservation.end_time - reservation.start_time).total_seconds() / 60 # in hours
#             amount_due = rental_duration * reservation.vehicle.hourly_rate
#             battery_depleted = 2* rental_duration
#             battery -= battery_depleted

#             # Record the payment with status as "Pending"
#             Payment.objects.create(
#                 user=request.user,
#                 amount=amount_due,
#                 status='Pending',  # Set payment status to "Pending"
#                 reservation=reservation
#             )

#             messages.success(request, f"You have successfully returned {reservation.vehicle.vehicle_name}. Payment of ${amount_due:.2f} has been recorded as pending.")
#             return redirect('customer_dashboard')

#         elif action_type == 'report':
#             issue_type = request.POST.get('issue_type')
#             comments = request.POST.get('comments')

#             # Create a report for the vehicle
#             Report.objects.create(
#                 vehicle=reservation.vehicle,
#                 user=request.user,
#                 reason=issue_type,
#                 comment=comments
#             )

#             # Mark vehicle as defective and update reservation
#             reservation.vehicle.is_defective = True
#             reservation.vehicle.is_available = False  # Mark the vehicle as unavailable for repairs
#             reservation.vehicle.latitude = latitude
#             reservation.vehicle.longitude = longitude
#             reservation.vehicle.battery = battery_depleted
#             reservation.vehicle.save()

#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.save()

#             messages.success(request, f"You have reported an issue with {reservation.vehicle.vehicle_name}. The vehicle has been marked for maintenance.")
#             return redirect('customer_dashboard')

#     context = {
#         'reservations': reservations
#     }
#     return render(request, 'customers/return.html', context)


# # views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
# from django.contrib.auth.decorators import login_required
# from .models import Payment, User

# @login_required
# def payments(request):
#     user = request.user
#     pending_payments = Payment.objects.filter(user=user, status='Pending')
#     context = {
#         'payments': pending_payments,
#     }
#     return render(request, 'customers/payments.html', context)

# @login_required
# def make_payment(request, transaction_id):
#     payment = get_object_or_404(Payment, pk=transaction_id, user=request.user)
#     user = request.user

#     if user.balance >= payment.amount:
#         # Deduct the payment amount from user's balance
#         user.balance -= payment.amount
#         user.save()

#         # Update payment status to 'Completed'
#         payment.status = 'Completed'
#         payment.save()

#         messages.success(request, 'Payment completed successfully.')
#     else:
#         messages.error(request, 'Insufficient funds. Please add more funds to your account.')

#     return redirect('payments')

# @login_required
# def add_funds(request):
#     if request.method == 'POST':
#         # Assuming that the form is validated properly
#         amount = float(request.POST['amount'])
#         user = request.user
#         user.balance += amount
#         user.save()
#         messages.success(request, 'Funds added successfully.')
#         return redirect('payments')

#     return render(request, 'customers/add_funds.html')

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import Payment, Reservation

# @login_required(login_url='login')
# def transaction_history(request):
#     user = request.user
#     payments = Payment.objects.filter(user=user)
#     context = {
#         'transactions': payments,
#     }
#     return render(request, 'customers/transaction_history.html', context)

# # customers/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from customers.models import Vehicle, Reservation, Report
# from django.utils import timezone
# from django.contrib import messages

# @login_required(login_url='login')
# def report_vehicle(request, reservation_id):
#     # Fetch the reservation that belongs to the user and is currently 'In use'
#     try:
#         reservation = Reservation.objects.get(pk=reservation_id, user=request.user, status='In use')
#     except Reservation.DoesNotExist:
#         messages.error(request, "Reservation not found or vehicle is not in use.")
#         return redirect('customer_dashboard')

#     if request.method == 'POST':
#         action_type = request.POST.get('action_type')

#         if action_type == 'return':
#             # Return Vehicle Logic
#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.vehicle.is_available = True
#             reservation.vehicle.save()
#             reservation.save()

#             messages.success(request, f"You have successfully returned {reservation.vehicle.vehicle_name}.")
#             return redirect('customer_dashboard')

#         elif action_type == 'report':
#             # Report Vehicle Logic
#             issue_type = request.POST.get('issue_type')
#             comments = request.POST.get('comments', '')

#             # Create a report for the vehicle
#             Report.objects.create(
#                 vehicle=reservation.vehicle,
#                 user=request.user,
#                 reason=issue_type,
#                 comment=comments
#             )

#             # Mark vehicle as defective and update reservation
#             reservation.vehicle.is_defective = True
#             reservation.vehicle.is_available = False
#             reservation.vehicle.save()
#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.save()

#             messages.success(request, f"You have reported an issue with {reservation.vehicle.vehicle_name}. The vehicle has been marked for maintenance.")
#             return redirect('customer_dashboard')

#     context = {
#         'reservation': reservation
#     }
#     return render(request, 'customers/return.html', context)]



# second code
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from django.contrib import messages
# from django.urls import reverse
# from customers.models import User, Vehicle, Reservation, Payment, Report
# import json
# import threading
# import time

# # Function to decrease battery level every 100ms
# def decrease_battery(vehicle):
#     while vehicle.battery > 0:
#         vehicle.battery -= 2
#         if vehicle.battery < 0:
#             vehicle.battery = 0
#         vehicle.save()
#         time.sleep(0.1)  # 100 milliseconds

# @login_required(login_url='login')
# def customer_dashboard(request):
#     user = request.user
#     reservations = Reservation.objects.filter(user=user)
#     payments = Payment.objects.filter(user=user)

#     context = {
#         'user': user,
#         'reservations': reservations,
#         'payments': payments
#     }

#     return render(request, 'customers/dashboard.html', context)

# @login_required(login_url='login')
# def rent_vehicle(request):
#     vehicles = Vehicle.objects.filter(is_available=True)

#     vehicles_list = [
#         {
#             "vehicle_id": vehicle.vehicle_id,
#             "vehicle_name": vehicle.vehicle_name,
#             "vehicle_type": vehicle.vehicle_type,
#             "battery": vehicle.battery,
#             "hourly_rate": vehicle.hourly_rate,
#             "latitude": vehicle.latitude,
#             "longitude": vehicle.longitude
#         }
#         for vehicle in vehicles
#     ]
#     vehicles_json = json.dumps(vehicles_list)

#     if request.method == "POST":
#         vehicle_id = request.POST.get("vehicle_id")
#         try:
#             vehicle = Vehicle.objects.get(pk=vehicle_id, is_available=True)
#         except Vehicle.DoesNotExist:
#             messages.error(request, "The selected vehicle is no longer available.")
#             return redirect('rent_vehicle')

#         reservation = Reservation.objects.create(
#             vehicle=vehicle,
#             user=request.user,
#             start_time=timezone.now(),
#             status='In use'
#         )

#         vehicle.is_available = False
#         vehicle.save()

#         # Start the battery depletion thread
#         threading.Thread(target=decrease_battery, args=(vehicle,), daemon=True).start()

#         messages.success(request, f"You have successfully rented {vehicle.vehicle_name}.")
#         return redirect('customer_dashboard')

#     context = {
#         "vehicles": vehicles,
#         "vehicles_json": vehicles_json
#     }

#     return render(request, 'customers/rent.html', context)

# @login_required(login_url='login')
# def return_vehicle(request):
#     reservations = Reservation.objects.filter(user=request.user, status='In use')

#     if request.method == 'POST':
#         reservation_id = request.POST.get('reservation_id')
#         action_type = request.POST.get('action_type')
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')

#         try:
#             reservation = Reservation.objects.get(pk=reservation_id, user=request.user, status='In use')
#         except Reservation.DoesNotExist:
#             messages.error(request, "Reservation not found or vehicle is not in use.")
#             return redirect('return_vehicle')

#         if action_type == 'return':
#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.vehicle.is_available = True

#             if latitude and longitude:
#                 reservation.vehicle.latitude = latitude
#                 reservation.vehicle.longitude = longitude

#             reservation.vehicle.save()
#             reservation.save()

#             rental_duration = (reservation.end_time - reservation.start_time).total_seconds() / 3600  # in hours
#             amount_due = rental_duration * reservation.vehicle.hourly_rate
#             battery_depleted = reservation.vehicle.battery

#             Payment.objects.create(
#                 user=request.user,
#                 amount=amount_due,
#                 status='Pending',
#                 reservation=reservation
#             )

#             messages.success(request, f"You have successfully returned {reservation.vehicle.vehicle_name}. Payment of ${amount_due:.2f} has been recorded as pending.")
#             return redirect('customer_dashboard')

#         elif action_type == 'report':
#             issue_type = request.POST.get('issue_type')
#             comments = request.POST.get('comments')

#             Report.objects.create(
#                 vehicle=reservation.vehicle,
#                 user=request.user,
#                 reason=issue_type,
#                 comment=comments
#             )

#             reservation.vehicle.is_defective = True
#             reservation.vehicle.is_available = False
#             reservation.vehicle.latitude = latitude
#             reservation.vehicle.longitude = longitude
#             reservation.vehicle.battery = 0
#             reservation.vehicle.save()

#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.save()

#             messages.success(request, f"You have reported an issue with {reservation.vehicle.vehicle_name}. The vehicle has been marked for maintenance.")
#             return redirect('customer_dashboard')

#     context = {
#         'reservations': reservations
#     }
#     return render(request, 'customers/return.html', context)

# @login_required
# def payments(request):
#     user = request.user
#     pending_payments = Payment.objects.filter(user=user, status='Pending')
#     context = {
#         'payments': pending_payments,
#     }
#     return render(request, 'customers/payments.html', context)

# @login_required
# def make_payment(request, transaction_id):
#     payment = get_object_or_404(Payment, pk=transaction_id, user=request.user)
#     user = request.user

#     if user.balance >= payment.amount:
#         user.balance -= payment.amount
#         user.save()

#         payment.status = 'Completed'
#         payment.save()

#         messages.success(request, 'Payment completed successfully.')
#     else:
#         messages.error(request, 'Insufficient funds. Please add more funds to your account.')

#     return redirect('payments')

# @login_required
# def add_funds(request):
#     if request.method == 'POST':
#         amount = float(request.POST['amount'])
#         user = request.user
#         user.balance += amount
#         user.save()
#         messages.success(request, 'Funds added successfully.')
#         return redirect('payments')

#     return render(request, 'customers/add_funds.html')

# @login_required(login_url='login')
# def transaction_history(request):
#     user = request.user
#     payments = Payment.objects.filter(user=user)
#     context = {
#         'transactions': payments,
#     }
#     return render(request, 'customers/transaction_history.html', context)

# @login_required(login_url='login')
# def report_vehicle(request, reservation_id):
#     try:
#         reservation = Reservation.objects.get(pk=reservation_id, user=request.user, status='In use')
#     except Reservation.DoesNotExist:
#         messages.error(request, "Reservation not found or vehicle is not in use.")
#         return redirect('customer_dashboard')

#     if request.method == 'POST':
#         action_type = request.POST.get('action_type')

#         if action_type == 'return':
#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.vehicle.is_available = True
#             reservation.vehicle.save()
#             reservation.save()

#             messages.success(request, f"You have successfully returned {reservation.vehicle.vehicle_name}.")
#             return redirect('customer_dashboard')

#         elif action_type == 'report':
#             issue_type = request.POST.get('issue_type')
#             comments = request.POST.get('comments', '')

#             Report.objects.create(
#                 vehicle=reservation.vehicle,
#                 user=request.user,
#                 reason=issue_type,
#                 comment=comments
#             )

#             reservation.vehicle.is_defective = True
#             reservation.vehicle.is_available = False
#             reservation.vehicle.save()
#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.save()

#             messages.success(request, f"You have reported an issue with {reservation.vehicle.vehicle_name}. The vehicle has been marked for maintenance.")
#             return redirect('customer_dashboard')

#     context = {
#         'reservation': reservation
#     }
#     return render(request, 'customers/return.html', context)

# third code
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from django.contrib import messages
# from django.urls import reverse
# from customers.models import User, Vehicle, Reservation, Payment, Report
# import json
# import threading
# import time
# import math

# # Function to decrease battery level to fully deplete in 5 minutes
# def decrease_battery(vehicle):
#     depletion_rate = round( 100 / (5 * 60)  , 2)  # Deplete 100% battery in 5 minutes (5 * 60 seconds)
#     while vehicle.battery > 0:
#         vehicle.battery = round(vehicle.battery-depletion_rate, 2)
#         if vehicle.battery < 0:
#             vehicle.battery = 0
#         if vehicle.battery == 0:
#             vehicle.is_available = False
#         vehicle.save()
#         time.sleep(1)  # 1 second interval

# @login_required(login_url='login')
# def customer_dashboard(request):
#     user = request.user
#     reservations = Reservation.objects.filter(user=user, status="in use")
#     payments = Payment.objects.filter(user=user, status="pending")

#     context = {
#         'user': user,
#         'reservations': reservations,
#         'payments': payments
#     }

#     return render(request, 'customers/dashboard.html', context)


# @login_required(login_url='login')
# def rent_vehicle(request):
#     vehicles = Vehicle.objects.filter(is_available=True)

#     vehicles_list = [
#         {
#             "vehicle_id": vehicle.vehicle_id,
#             "vehicle_name": vehicle.vehicle_name,
#             "vehicle_type": vehicle.vehicle_type,
#             "battery": vehicle.battery,
#             "hourly_rate": vehicle.hourly_rate,
#             "latitude": vehicle.latitude,
#             "longitude": vehicle.longitude
#         }
#         for vehicle in vehicles
#     ]
#     vehicles_json = json.dumps(vehicles_list)

#     if request.method == "POST":
#         vehicle_id = request.POST.get("vehicle_id")
#         try:
#             vehicle = Vehicle.objects.get(pk=vehicle_id, is_available=True)
#         except Vehicle.DoesNotExist:
#             messages.error(request, "The selected vehicle is no longer available.")
#             return redirect('rent_vehicle')

#         reservation = Reservation.objects.create(
#             vehicle=vehicle,
#             user=request.user,
#             start_time=timezone.now(),
#             status='In use'
#         )

#         vehicle.is_available = False
#         vehicle.save()

#         # Start the battery depletion thread
#         threading.Thread(target=decrease_battery, args=(vehicle,), daemon=True).start()

#         messages.success(request, f"You have successfully rented {vehicle.vehicle_name}.")
#         return redirect('customer_dashboard')

#     context = {
#         "vehicles": vehicles,
#         "vehicles_json": vehicles_json
#     }

#     return render(request, 'customers/rent.html', context)

# @login_required(login_url='login')
# def return_vehicle(request):
#     reservations = Reservation.objects.filter(user=request.user, status='In use')

#     if request.method == 'POST':
#         reservation_id = request.POST.get('reservation_id')
#         action_type = request.POST.get('action_type')
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')

#         try:
#             reservation = Reservation.objects.get(pk=reservation_id, user=request.user, status='In use')
#         except Reservation.DoesNotExist:
#             messages.error(request, "Reservation not found or vehicle is not in use.")
#             return redirect('return_vehicle')

#         if action_type == 'return':
#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.vehicle.is_available = True

#             if latitude and longitude:
#                 reservation.vehicle.latitude = latitude
#                 reservation.vehicle.longitude = longitude
            
#             if reservation.vehicle.battery == 0:
#                 reservation.vehicle.is_available = False

#             reservation.vehicle.save()
#             reservation.save()

#             rental_duration = (reservation.end_time - reservation.start_time).total_seconds() / 60  # in hours
#             amount_due = round(rental_duration * reservation.vehicle.hourly_rate, 2)

#             Payment.objects.create(
#                 user=request.user,
#                 amount=amount_due,
#                 status='Pending',
#                 reservation=reservation
#             )

#             messages.success(request, f"You have successfully returned {reservation.vehicle.vehicle_name}. Payment of ${amount_due:.2f} has been recorded as pending.")
#             return redirect('customer_dashboard')

#         elif action_type == 'report':
#             issue_type = request.POST.get('issue_type')
#             comments = request.POST.get('comments')

#             Report.objects.create(
#                 vehicle=reservation.vehicle,
#                 user=request.user,
#                 reason=issue_type,
#                 comment=comments
#             )

#             reservation.vehicle.is_defective = True
#             reservation.vehicle.is_available = False
#             reservation.vehicle.latitude = latitude
#             reservation.vehicle.longitude = longitude
#             reservation.vehicle.save()

#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.save()

#             messages.success(request, f"You have reported an issue with {reservation.vehicle.vehicle_name}. The vehicle has been marked for maintenance.")
#             return redirect('customer_dashboard')

#     context = {
#         'reservations': reservations
#     }
#     return render(request, 'customers/return.html', context)

# @login_required
# def payments(request):
#     user = request.user
#     pending_payments = Payment.objects.filter(user=user, status='Pending')
#     context = {
#         'payments': pending_payments,
#     }
#     return render(request, 'customers/payments.html', context)

# @login_required
# def make_payment(request, transaction_id):
#     payment = get_object_or_404(Payment, pk=transaction_id, user=request.user)
#     user = request.user

#     if user.balance >= payment.amount:
#         user.balance -= payment.amount
#         user.save()

#         payment.status = 'Completed'
#         payment.save()

#         messages.success(request, 'Payment completed successfully.')
#     else:
#         messages.error(request, 'Insufficient funds. Please add more funds to your account.')

#     return redirect('payments')

# @login_required
# def add_funds(request):
#     if request.method == 'POST':
#         amount = float(request.POST['amount'])
#         user = request.user
#         user.balance += amount
#         user.save()
#         messages.success(request, 'Funds added successfully.')
#         return redirect('payments')

#     return render(request, 'customers/add_funds.html')

# @login_required(login_url='login')
# def transaction_history(request):
#     user = request.user
#     payments = Payment.objects.filter(user=user)
#     context = {
#         'transactions': payments,
#     }
#     return render(request, 'customers/transaction_history.html', context)

# @login_required(login_url='login')
# def report_vehicle(request, reservation_id):
#     try:
#         reservation = Reservation.objects.get(pk=reservation_id, user=request.user, status='In use')
#     except Reservation.DoesNotExist:
#         messages.error(request, "Reservation not found or vehicle is not in use.")
#         return redirect('customer_dashboard')

#     if request.method == 'POST':
#         action_type = request.POST.get('action_type')

#         if action_type == 'return':
#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.vehicle.is_available = True
#             reservation.vehicle.save(update_fields=['is_available'])
#             reservation.save()

#             messages.success(request, f"You have successfully returned {reservation.vehicle.vehicle_name}.")
#             return redirect('customer_dashboard')

#         elif action_type == 'report':
#             issue_type = request.POST.get('issue_type')
#             comments = request.POST.get('comments', '')

#             Report.objects.create(
#                 vehicle=reservation.vehicle,
#                 user=request.user,
#                 reason=issue_type,
#                 comment=comments
#             )

#             reservation.vehicle.is_defective = True
#             reservation.vehicle.is_available = False
#             reservation.vehicle.save(update_fields=['is_available'])
#             reservation.end_time = timezone.now()
#             reservation.status = 'Completed'
#             reservation.save()

#             messages.success(request, f"You have reported an issue with {reservation.vehicle.vehicle_name}. The vehicle has been marked for maintenance.")
#             return redirect('customer_dashboard')

#     context = {
#         'reservation': reservation
#     }
#     return render(request, 'customers/return.html', context)
# 4th code above

# Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from customers.models import User, Vehicle, Reservation, Payment, Report
import json
import threading
import time
import math

# Function to decrease battery level to fully deplete in 5 minutes
def decrease_battery(vehicle):
    depletion_rate = round(100 / (5 * 60), 2)  # Deplete 100% battery in 5 minutes (5 * 60 seconds)
    while vehicle.battery > 0:
        vehicle.battery = round(vehicle.battery - depletion_rate, 2)
        if vehicle.battery < 0:
            vehicle.battery = 0
        if vehicle.battery == 0:
            vehicle.is_available = False
        vehicle.save()
        time.sleep(1)  # 1 second interval

# Customer dashboard view
@login_required(login_url='login')
def customer_dashboard(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user, status="in use")
    payments = Payment.objects.filter(user=user, status="Pending")

    context = {
        'user': user,
        'reservations': reservations,
        'payments': payments
    }

    return render(request, 'customers/dashboard.html', context)

# View to rent a vehicle
@login_required(login_url='login')
def rent_vehicle(request):
    vehicles = Vehicle.objects.filter(is_available=True)

    # Convert vehicle details to JSON for rendering on the front end
    vehicles_list = [
        {
            "vehicle_id": vehicle.vehicle_id,
            "vehicle_name": vehicle.vehicle_name,
            "vehicle_type": vehicle.vehicle_type,
            "battery": vehicle.battery,
            "hourly_rate": vehicle.hourly_rate,
            "latitude": vehicle.latitude,
            "longitude": vehicle.longitude
        }
        for vehicle in vehicles
    ]
    vehicles_json = json.dumps(vehicles_list)

    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle_id")
        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id, is_available=True)
        except Vehicle.DoesNotExist:
            messages.error(request, "The selected vehicle is no longer available.")
            return redirect('rent_vehicle')

        # Create a reservation for the selected vehicle
        reservation = Reservation.objects.create(
            vehicle=vehicle,
            user=request.user,
            start_time=timezone.now(),
            status='In use'
        )

        vehicle.is_available = False
        vehicle.save()

        # Start the battery depletion thread
        threading.Thread(target=decrease_battery, args=(vehicle,), daemon=True).start()

        messages.success(request, f"You have successfully rented {vehicle.vehicle_name}.")
        return redirect('customer_dashboard')

    context = {
        "vehicles": vehicles,
        "vehicles_json": vehicles_json
    }

    return render(request, 'customers/rent.html', context)

# View to return a rented vehicle
@login_required(login_url='login')
def return_vehicle(request):
    reservations = Reservation.objects.filter(user=request.user, status='In use')

    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        action_type = request.POST.get('action_type')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        try:
            reservation = Reservation.objects.get(pk=reservation_id, user=request.user, status='In use')
        except Reservation.DoesNotExist:
            messages.error(request, "Reservation not found or vehicle is not in use.")
            return redirect('return_vehicle')

        if action_type == 'return':
            # Update reservation status to 'Completed'
            reservation.end_time = timezone.now()
            reservation.status = 'Completed'
            reservation.vehicle.is_available = True

            if latitude and longitude:
                reservation.vehicle.latitude = latitude
                reservation.vehicle.longitude = longitude

            if reservation.vehicle.battery == 0:
                reservation.vehicle.is_available = False

            reservation.vehicle.save()
            reservation.save()

            # Calculate amount due based on rental duration and hourly rate
            rental_duration = (reservation.end_time - reservation.start_time).total_seconds() / 60  # in hours
            amount_due = round(rental_duration * reservation.vehicle.hourly_rate, 2)

            Payment.objects.create(
                user=request.user,
                amount=amount_due,
                status='Pending',
                reservation=reservation
            )

            messages.success(request, f"You have successfully returned {reservation.vehicle.vehicle_name}. Payment of ${amount_due:.2f} has been recorded as pending.")
            return redirect('customer_dashboard')

        elif action_type == 'report':
            # Create a report for the vehicle
            issue_type = request.POST.get('issue_type')
            comments = request.POST.get('comments')

            Report.objects.create(
                vehicle=reservation.vehicle,
                user=request.user,
                reason=issue_type,
                comment=comments
            )

            reservation.vehicle.is_defective = True
            reservation.vehicle.is_available = False
            reservation.vehicle.latitude = latitude
            reservation.vehicle.longitude = longitude
            reservation.vehicle.save()

            reservation.end_time = timezone.now()
            reservation.status = 'Completed'
            reservation.save()

            messages.success(request, f"You have reported an issue with {reservation.vehicle.vehicle_name}. The vehicle has been marked for maintenance.")
            return redirect('customer_dashboard')

    context = {
        'reservations': reservations
    }
    return render(request, 'customers/return.html', context)

# View to display pending payments
@login_required
def payments(request):
    user = request.user
    pending_payments = Payment.objects.filter(user=user, status='Pending')
    context = {
        'payments': pending_payments,
    }
    return render(request, 'customers/payments.html', context)

# View to make a payment for a specific transaction
@login_required
def make_payment(request, transaction_id):
    payment = get_object_or_404(Payment, pk=transaction_id, user=request.user)
    user = request.user

    if user.balance >= payment.amount:
        user.balance -= payment.amount
        user.save()

        payment.status = 'Completed'
        payment.save()

        messages.success(request, 'Payment completed successfully.')
    else:
        messages.error(request, 'Insufficient funds. Please add more funds to your account.')

    return redirect('payments')

# View to add funds to user's balance
@login_required
def add_funds(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        user = request.user
        user.balance += amount
        user.save()
        messages.success(request, 'Funds added successfully.')
        return redirect('payments')

    return render(request, 'customers/add_funds.html')

# View to display transaction history
@login_required(login_url='login')
def transaction_history(request):
    user = request.user
    payments = Payment.objects.filter(user=user)
    context = {
        'transactions': payments,
    }
    return render(request, 'customers/transaction_history.html', context)

# View to report an issue with a vehicle
@login_required(login_url='login')
def report_vehicle(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id, user=request.user, status='In use')
    except Reservation.DoesNotExist:
        messages.error(request, "Reservation not found or vehicle is not in use.")
        return redirect('customer_dashboard')

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        if action_type == 'return':
            reservation.end_time = timezone.now()
            reservation.status = 'Completed'
            reservation.vehicle.is_available = True
            reservation.vehicle.save(update_fields=['is_available'])
            reservation.save()

            messages.success(request, f"You have successfully returned {reservation.vehicle.vehicle_name}.")
            return redirect('customer_dashboard')

        elif action_type == 'report':
            # Create a report for the vehicle
            issue_type = request.POST.get('issue_type')
            comments = request.POST.get('comments', '')

            Report.objects.create(
                vehicle=reservation.vehicle,
                user=request.user,
                reason=issue_type,
                comment=comments
            )

            reservation.vehicle.is_defective = True
            reservation.vehicle.is_available = False
            reservation.vehicle.save(update_fields=['is_available'])
            reservation.end_time = timezone.now()
            reservation.status = 'Completed'
            reservation.save()

            messages.success(request, f"You have reported an issue with {reservation.vehicle.vehicle_name}. The vehicle has been marked for maintenance.")
            return redirect('customer_dashboard')

    context = {
        'reservation': reservation
    }
    return render(request, 'customers/return.html', context)
