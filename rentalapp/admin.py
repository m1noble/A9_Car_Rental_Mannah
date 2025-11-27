from django.contrib import admin
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

# Register all models so TA can see CRUD in admin
admin.site.register(Customer)
admin.site.register(VehicleType)
admin.site.register(Employee)
admin.site.register(Vehicle)
admin.site.register(Reservation)
admin.site.register(Rental)
admin.site.register(Payment)
admin.site.register(Maintenance)
admin.site.register(InsurancePolicy)
