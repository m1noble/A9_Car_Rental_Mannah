from django.db import models


# ---------------------------
# Customer Table
# ---------------------------
class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    driver_license = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.customer_id} - {self.name}"


# ---------------------------
# Vehicle Type Table
# ---------------------------
class VehicleType(models.Model):
    vehicletype_id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=50)
    seats_num = models.IntegerField()
    daily_rate = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.vehicletype_id} - {self.category}"


# ---------------------------
# Employee Table
# ---------------------------
class Employee(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.employee_id} - {self.name}"


# ---------------------------
# Vehicle Table
# ---------------------------
class Vehicle(models.Model):
    vehicle_id = models.IntegerField(primary_key=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    mileage = models.IntegerField()
    plate = models.CharField(max_length=30, unique=True)
    vehicletype = models.ForeignKey(VehicleType, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.vehicle_id} - {self.make} {self.model}"


# ---------------------------
# Reservation Table
# ---------------------------
class Reservation(models.Model):
    reservation_id = models.IntegerField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    reservation_date = models.DateField()
    availability_status = models.CharField(max_length=30, blank=True, null=True)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.reservation_id}"


# ---------------------------
# Rental Table
# ---------------------------
class Rental(models.Model):
    rental_id = models.IntegerField(primary_key=True)
    rental_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.rental_id}"


# ---------------------------
# Payment Table
# ---------------------------
class Payment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    charge_due = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=30, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)

    rental = models.ForeignKey(Rental, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.payment_id}"


# ---------------------------
# Maintenance Table
# ---------------------------
class Maintenance(models.Model):
    maintenance_id = models.IntegerField(primary_key=True)
    service_date = models.DateField()
    description = models.CharField(max_length=400, blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2)

    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.maintenance_id}"


# ---------------------------
# Insurance Policy Table
# ---------------------------
class InsurancePolicy(models.Model):
    insurance_id = models.IntegerField(primary_key=True)
    policy_number = models.CharField(max_length=50, unique=True)
    coverage_type = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=100, blank=True, null=True)

    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.insurance_id} - {self.policy_number}"
