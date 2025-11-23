# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import Count, Sum
# from customers.models import Vehicle, Reservation, Payment, Report, User
# from operators.models import MaintenanceRecord, ChargingRecord
# from datetime import timedelta, datetime
# from django.utils import timezone

# @login_required(login_url='login')
# def manager_dashboard(request):
#     # Get start and end date from GET request, default to last week until now
#     end_date_str = request.GET.get('end_date', timezone.now().date().isoformat())
#     start_date_str = request.GET.get('start_date', (timezone.now() - timedelta(days=7)).date().isoformat())

#     # Convert string dates to datetime.date objects
#     try:
#         start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#         end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#     except ValueError:
#         start_date = (timezone.now() - timedelta(days=7)).date()
#         end_date = timezone.now().date()

#     # Vehicle Utilization Over Time
#     reservations = Reservation.objects.filter(start_time__date__range=(start_date, end_date))
#     vehicle_usage_data = reservations.extra({'date': 'date(start_time)'}).values('date').annotate(total=Count('vehicle_id'))

#     # Revenue Generated Over Time
#     payments = Payment.objects.filter(created_at__date__range=(start_date, end_date), status='Completed')
#     revenue_data = payments.extra({'date': 'date(created_at)'}).values('date').annotate(total=Sum('amount'))

#     # Battery Status Distribution
#     battery_data = Vehicle.objects.values('battery').annotate(count=Count('battery'))

#     # Maintenance Record Summary
#     maintenance_records = MaintenanceRecord.objects.filter(maintenance_date__date__range=(start_date, end_date))
#     maintenance_data = maintenance_records.extra({'date': 'date(maintenance_date)'}).values('date').annotate(total=Count('maintenance_id'))

#     # Charging Patterns
#     charge_records = ChargingRecord.objects.filter(charge_date__date__range=(start_date, end_date))
#     charge_data = charge_records.extra({'date': 'date(charge_date)'}).values('date').annotate(total=Count('charge_id'))

#     # User Registrations Over Time
#     user_registration_data = User.objects.filter(date_joined__date__range=(start_date, end_date)).extra({'date': 'date(date_joined)'}).values('date').annotate(total=Count('username'))

#     # Vehicle Availability Distribution
#     vehicle_availability_data = Vehicle.objects.values('is_available').annotate(total=Count('vehicle_id'))

#     # Report Statistics
#     reports_data = Report.objects.filter().values('reason').annotate(count=Count('report_id'))

#     context = {
#         'vehicle_usage_data': list(vehicle_usage_data),
#         'revenue_data': list(revenue_data),
#         'battery_data': list(battery_data),
#         'maintenance_data': list(maintenance_data),
#         'charge_data': list(charge_data),
#         'user_registration_data': list(user_registration_data),
#         'vehicle_availability_data': list(vehicle_availability_data),
#         'reports_data': list(reports_data),
#         'start_date': start_date,
#         'end_date': end_date,
#     }

#     return render(request, 'managers/dashboard.html', context)
#previous code

# Imports
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from customers.models import Vehicle, Reservation, Payment, Report, User
from operators.models import MaintenanceRecord, ChargingRecord
from datetime import timedelta, datetime
from django.utils import timezone

# Manager dashboard view
@login_required(login_url='login')
def manager_dashboard(request):
    # Get start and end date from GET request, default to last week until now
    end_date_str = request.GET.get('end_date', timezone.now().date().isoformat())
    start_date_str = request.GET.get('start_date', (timezone.now() - timedelta(days=7)).date().isoformat())

    # Convert string dates to datetime.date objects
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        start_date = (timezone.now() - timedelta(days=7)).date()
        end_date = timezone.now().date()

    # Vehicle Utilization Over Time
    reservations = Reservation.objects.filter(start_time__date__range=(start_date, end_date))
    vehicle_usage_data = reservations.extra({'date': 'date(start_time)'}).values('date').annotate(total=Count('vehicle_id'))

    # Revenue Generated Over Time
    payments = Payment.objects.filter(created_at__date__range=(start_date, end_date), status='Completed')
    revenue_data = payments.extra({'date': 'date(created_at)'}).values('date').annotate(total=Sum('amount'))

    # Battery Status Distribution
    battery_data = Vehicle.objects.values('battery').annotate(count=Count('battery'))

    # Maintenance Record Summary
    maintenance_records = MaintenanceRecord.objects.filter(maintenance_date__date__range=(start_date, end_date))
    maintenance_data = maintenance_records.extra({'date': 'date(maintenance_date)'}).values('date').annotate(total=Count('maintenance_id'))

    # Charging Patterns
    charge_records = ChargingRecord.objects.filter(charge_date__date__range=(start_date, end_date))
    charge_data = charge_records.extra({'date': 'date(charge_date)'}).values('date').annotate(total=Count('charge_id'))

    # User Registrations Over Time
    user_registration_data = User.objects.filter(date_joined__date__range=(start_date, end_date)).extra({'date': 'date(date_joined)'}).values('date').annotate(total=Count('username'))

    # Vehicle Availability Distribution
    vehicle_availability_data = Vehicle.objects.values('is_available').annotate(total=Count('vehicle_id'))

    # Report Statistics
    reports_data = Report.objects.filter().values('reason').annotate(count=Count('report_id'))

    # Prepare context for template rendering
    context = {
        'vehicle_usage_data': list(vehicle_usage_data),  # Data for vehicle usage over time
        'revenue_data': list(revenue_data),  # Data for revenue generated over time
        'battery_data': list(battery_data),  # Data for battery status distribution
        'maintenance_data': list(maintenance_data),  # Data for maintenance records over time
        'charge_data': list(charge_data),  # Data for charging records over time
        'user_registration_data': list(user_registration_data),  # Data for user registrations over time
        'vehicle_availability_data': list(vehicle_availability_data),  # Data for vehicle availability
        'reports_data': list(reports_data),  # Data for report statistics
        'start_date': start_date,  # Start date for filtering
        'end_date': end_date,  # End date for filtering
    }

    return render(request, 'managers/dashboard.html', context)
