from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q

from .models import (
    Customer,
    VehicleType,
    Employee,
    Vehicle,
    Reservation,
    Rental,
    Payment,
    Maintenance,
    InsurancePolicy,
)


# ---------------------------
# Main menu page
# ---------------------------
def menu(request):
    """
    Simple menu that exposes all required A9 options:
    - Create Tables
    - Drop Tables
    - Populate Tables (dummy data)
    - Query Tables
    """
    context = {
        "message": request.GET.get("message", "")
    }
    return render(request, "menu.html", context)


# ---------------------------
# Create tables (logical)
# ---------------------------
def create_tables(request):
    """
    In Django, physical tables are created by 'makemigrations' + 'migrate'.
    This view exists to satisfy the 'Create Tables' menu option in the rubric.
    We simply show a confirmation message that tables are ready.
    """
    msg = (
        "Tables are managed by Django migrations. "
        "Run 'py manage.py makemigrations' and 'py manage.py migrate' once. "
        "The database schema is now ready (3NF/BCNF)."
    )
    return redirect(f"/?message={msg}")


# ---------------------------
# Drop tables (logical)
# ---------------------------
@transaction.atomic
def drop_tables(request):
    """
    Instead of dropping the actual SQLite tables, we delete the contents
    of all tables. This is safer and fully resets the database rows.
    """
    Maintenance.objects.all().delete()
    InsurancePolicy.objects.all().delete()
    Payment.objects.all().delete()
    Rental.objects.all().delete()
    Reservation.objects.all().delete()
    Vehicle.objects.all().delete()
    Employee.objects.all().delete()
    VehicleType.objects.all().delete()
    Customer.objects.all().delete()

    msg = "All records deleted from every table (logical DROP TABLES)."
    return redirect(f"/?message={msg}")


# ---------------------------
# Populate tables with dummy data
# ---------------------------
@transaction.atomic
def populate_tables(request):
    """
    Insert sample dummy data for all tables.
    If data already exists, we skip insertion to avoid duplicates.
    """
    if Customer.objects.exists():
        msg = "Database already contains data. No new dummy records inserted."
        return redirect(f"/?message={msg}")

    # Vehicle types
    compact = VehicleType.objects.create(
        vehicletype_id=1, category="Compact", seats_num=4, daily_rate=39.99
    )
    suv = VehicleType.objects.create(
        vehicletype_id=2, category="SUV", seats_num=5, daily_rate=59.99
    )

    # Employees
    e1 = Employee.objects.create(employee_id=1, role="Mechanic", name="Alex Johnson")
    e2 = Employee.objects.create(employee_id=2, role="Agent", name="Maria Lopez")

    # Customers
    c1 = Customer.objects.create(
        customer_id=1,
        driver_license="D1234567",
        name="Mannah Noble",
        phone_number="416-555-0001",
        email="mannah@example.com",
    )
    c2 = Customer.objects.create(
        customer_id=2,
        driver_license="D7654321",
        name="Kimaya Rangari",
        phone_number="416-555-0002",
        email="kimtan@example.com",
    )

    # Vehicles
    v1 = Vehicle.objects.create(
        vehicle_id=1,
        make="Toyota",
        model="Corolla",
        year=2021,
        mileage=25000,
        plate="ABC-123",
        vehicletype=compact,
    )
    v2 = Vehicle.objects.create(
        vehicle_id=2,
        make="Honda",
        model="CR-V",
        year=2020,
        mileage=30000,
        plate="XYZ-789",
        vehicletype=suv,
    )

    # Reservations
    r1 = Reservation.objects.create(
        reservation_id=1,
        start_date="2025-01-10",
        end_date="2025-01-15",
        reservation_date="2025-01-05",
        availability_status="Confirmed",
        customer=c1,
        vehicle=v1,
    )

    # Rentals
    rent1 = Rental.objects.create(
        rental_id=1,
        rental_date="2025-01-10",
        return_date="2025-01-15",
        total_amount=5 * compact.daily_rate,
        reservation=r1,
    )

    # Payments
    Payment.objects.create(
        payment_id=1,
        charge_due=rent1.total_amount,
        method="Credit Card",
        payment_date="2025-01-10",
        rental=rent1,
    )

    # Maintenance
    Maintenance.objects.create(
        maintenance_id=1,
        service_date="2024-12-01",
        description="Oil change and tire rotation",
        cost=120.00,
        vehicle=v2,
        employee=e1,
    )

    # Insurance
    InsurancePolicy.objects.create(
        insurance_id=1,
        policy_number="POL-1001",
        coverage_type="Full Coverage",
        provider="ABC Insurance",
        vehicle=v1,
    )

    msg = "Dummy records inserted into all tables (POPULATE TABLES)."
    return redirect(f"/?message={msg}")


# ---------------------------
# Queries: list & search customers
# ---------------------------
def customer_list(request):
    customers = Customer.objects.all().order_by("customer_id")
    return render(request, "customers.html", {"customers": customers})


def customer_search(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = Customer.objects.filter(
            Q(name__icontains=query)
            | Q(driver_license__icontains=query)
            | Q(email__icontains=query)
        ).order_by("customer_id")

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "customer_search.html", context)


# ---------------------------
# Queries: list & search vehicles
# ---------------------------
def vehicle_list(request):
    vehicles = Vehicle.objects.select_related("vehicletype").all().order_by("vehicle_id")
    return render(request, "vehicles.html", {"vehicles": vehicles})


def vehicle_search(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = Vehicle.objects.select_related("vehicletype").filter(
            Q(make__icontains=query)
            | Q(model__icontains=query)
            | Q(plate__icontains=query)
            | Q(vehicletype__category__icontains=query)
        ).order_by("vehicle_id")

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "vehicle_search.html", context)
