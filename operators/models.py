# from django.db import models
# from customers.models import Vehicle, User
# from django.contrib.auth import get_user_model

# class ChargingRecord(models.Model):
#     charge_id = models.AutoField(primary_key=True)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     battery_charged = models.FloatField()
#     charge_date = models.DateTimeField(auto_now_add=True)
#     operator = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Charging Record {self.charge_id} for Vehicle {self.vehicle.vehicle_id}"

# class MaintenanceRecord(models.Model):
#     maintenance_id = models.AutoField(primary_key=True)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     maintenance_date = models.DateTimeField(auto_now_add=True)
#     operator = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Maintenance Record {self.maintenance_id} for Vehicle {self.vehicle.vehicle_id}"
#previous code

# Imports
from django.db import models
from customers.models import Vehicle, User
from django.contrib.auth import get_user_model

# Model to store charging records of vehicles
class ChargingRecord(models.Model):
    charge_id = models.AutoField(primary_key=True)  # Unique ID for each charging record
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)  # Reference to the vehicle being charged
    battery_charged = models.FloatField()  # Battery percentage charged
    charge_date = models.DateTimeField(auto_now_add=True)  # Date and time of charging (auto set to current)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)  # Operator responsible for charging

    def __str__(self):
        return f"Charging Record {self.charge_id} for Vehicle {self.vehicle.vehicle_id}"

# Model to store maintenance records of vehicles
class MaintenanceRecord(models.Model):
    maintenance_id = models.AutoField(primary_key=True)  # Unique ID for each maintenance record
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)  # Reference to the vehicle being maintained
    maintenance_date = models.DateTimeField(auto_now_add=True)  # Date and time of maintenance (auto set to current)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)  # Operator responsible for maintenance

    def __str__(self):
        return f"Maintenance Record {self.maintenance_id} for Vehicle {self.vehicle.vehicle_id}"
