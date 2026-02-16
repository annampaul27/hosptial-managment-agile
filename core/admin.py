from django.contrib import admin

# Register your models here.


from .models import (
    PatientProfile,
    DoctorProfile,
    LabTechnicianProfile,
    FrontDeskProfile,
    AdminProfile,
    Appointment,
    Prescription,
    Lab,
    DiagnosticTest,
    TestBooking,
    LabResult,
    Payment,
    LoginHistory,
    PatientHistory
)

admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(LabTechnicianProfile)
admin.site.register(FrontDeskProfile)
admin.site.register(AdminProfile)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Lab)
admin.site.register(DiagnosticTest)
admin.site.register(TestBooking)
admin.site.register(LabResult)
admin.site.register(Payment)
admin.site.register(LoginHistory)
admin.site.register(PatientHistory)

# Add this to your admin.py file
