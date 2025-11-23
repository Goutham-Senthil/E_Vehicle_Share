from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from customers.models import User, Vehicle, Reservation, Payment
from django.utils import timezone
import json
from customers.models import Vehicle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customers.models import Vehicle, Reservation
from django.http import HttpResponse
from .models import Vehicle, ChargingRecord, MaintenanceRecord


@login_required
def operator_dashboard(request):
    # Fetch all vehicles assigned to the operator that are defective and not in use
    defective_vehicles = Vehicle.objects.filter(is_defective=True).exclude(reservation__status='In use')
    # Fetch all vehicles that need charging (battery level less than 100%) and not in use
    vehicles_needing_charge = Vehicle.objects.filter(battery__lt=100).exclude(reservation__status='In use')
    context = {
        'user': request.user,
        'vehicles': defective_vehicles,
        'vehicles_needing_charge': vehicles_needing_charge,
    }
    return render(request, 'operators/dashboard.html', context)

@login_required
def repair_vehicle(request, vehicle_id):
    # Fetch the vehicle that matches the given vehicle_id
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    
    # Only proceed if the vehicle is defective
    if vehicle.is_defective:
        # Update vehicle status to repaired
        vehicle.is_defective = False
        vehicle.is_available = True
        vehicle.save()
        
        # Record the maintenance action
        MaintenanceRecord.objects.create(
            vehicle=vehicle,
            maintenance_date=timezone.now(),
            operator=request.user
        )
    
    # Redirect back to the operator dashboard after repair action
    return redirect('operator_dashboard')

@login_required
def charge_vehicle(request, vehicle_id):
    # Fetch the vehicle that matches the given vehicle_id
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    
    # Only proceed if the vehicle's battery is less than 100%
    if vehicle.battery == 0:

        vehicle.battery = 100
        vehicle.is_available = True
        vehicle.save()

        ChargingRecord.objects.create(
            vehicle=vehicle,
            battery_charged=100,
            charge_date=timezone.now(),
            operator=request.user
        )

    elif vehicle.battery < 100:
        # Charge the vehicle to 100%
        battery_charged =100-vehicle.battery
        vehicle.battery = 100
        vehicle.save()
        
        # Record the charging action
        ChargingRecord.objects.create(
            vehicle=vehicle,
            battery_charged=battery_charged,
            charge_date=timezone.now(),
            operator=request.user
        )
    
    # Redirect back to the operator dashboard after charging action
    return redirect('operator_dashboard')


@login_required(login_url='login')
def move_vehicle(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        new_longitude = request.POST.get('new_longitude')
        new_latitude = request.POST.get('new_latitude')

        try:
            # Retrieve the vehicle object
            vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
            
            # Update the vehicle location
            vehicle.longitude = new_longitude
            vehicle.latitude = new_latitude
            vehicle.save()

            return JsonResponse({'message': f'Vehicle {vehicle.vehicle_id} has been successfully moved to the new location.'})
        except Vehicle.DoesNotExist:
            return JsonResponse({'message': 'Vehicle not found.'}, status=404)
    
    # Render the map with vehicles data
    vehicles = Vehicle.objects.all()
    return render(request, 'operators/move_vehicles.html', {'vehicles': vehicles})

@login_required(login_url='login')
def track_vehicle(request):
    # Fetch all vehicle data
    vehicles = Vehicle.objects.all()
    vehicles_list = []

    for vehicle in vehicles:
        vehicle_info = {
            "vehicle_id": vehicle.vehicle_id,
            "vehicle_name": vehicle.vehicle_name,
            "vehicle_type": vehicle.vehicle_type,
            "vehicle_model": vehicle.vehicle_model,
            "longitude": vehicle.longitude,
            "latitude": vehicle.latitude,
            "battery": vehicle.battery,
            "is_in_use": False,
            "user_name": ""
        }

        # Check if the vehicle is currently reserved
        reservation = Reservation.objects.filter(vehicle=vehicle, status='In use').first()
        if reservation:
            vehicle_info["is_in_use"] = True
            vehicle_info["user_name"] = f"{reservation.user.first_name} {reservation.user.surname}"

        vehicles_list.append(vehicle_info)

    vehicles_json = json.dumps(vehicles_list)

    context = {
        'vehicles_json': vehicles_json,
        'vehicles': vehicles,
    }

    return render(request, 'operators/track_vehicle.html', context)

@login_required(login_url='login')
def maintenance_record(request):
    # Fetch all maintenance records
    records = MaintenanceRecord.objects.all()
    context = {
        'records': records,
    }
    return render(request, 'operators/maintenance_record.html', context)

@login_required(login_url='login')
def charge_record(request):
    # Fetch all charge records
    records = ChargingRecord.objects.all()
    context = {
        'records': records,
    }
    return render(request, 'operators/charge_record.html', context)