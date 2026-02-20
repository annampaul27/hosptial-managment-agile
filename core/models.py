from datetime import date

from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#Patient Profile
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, unique=True)
    gender = models.CharField(max_length=10, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="Active")
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        null=True,
        blank=True
    )


    @property
    def age(self):
        if not self.dob:
            return None
        today = date.today()
        return (
            today.year
            - self.dob.year
            - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )
    
    def __str__(self):
        return self.full_name


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    
    # Professional details
    license_number = models.CharField(max_length=50, blank=True, default="")
    experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    consultation_fee = models.DecimalField(
    max_digits=8, 
    decimal_places=2, 
    default=0.00,  # default value for new and existing rows
    help_text="Fee in INR"
)

    
    # Contact info
    phone = models.CharField(max_length=15)
    
    # Additional info
    bio = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="Active")

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.specialization})"


#Front Desk (Reception)
class FrontDeskProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default="Active")

    def __str__(self):
        return self.user.username


#Admin Profile
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


#Appointments
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending Payment', 'Pending Payment'),  # Initial status when appointment is created
        ('Scheduled', 'Scheduled'),              # After payment is completed
        ('Confirmed', 'Confirmed'),              # Doctor confirmed
        ('Completed', 'Completed'),              # Appointment finished
        ('Cancelled', 'Cancelled'),              # Appointment cancelled
        ('No Show', 'No Show'),                  # Patient didn't show up
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending Payment"  # Changed default
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.full_name} - Dr. {self.doctor.user.get_full_name()} ({self.status})"


#Prescriptions
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

#Labs
class Lab(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=150)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class LabTechnicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default="Active")

    bio = models.TextField(blank=True, null=True)  # ✅ New field

    def __str__(self):
        return self.user.username


#Diagnostic Tests
class DiagnosticTest(models.Model):

    CATEGORY_CHOICES = [
        ('Blood Tests', 'Blood Tests'),
        ('Urine Tests', 'Urine Tests'),
        ('Imaging', 'Imaging'),
        ('Screening', 'Screening'),
        ('General', 'General'),
    ]

    SAMPLE_TYPE_CHOICES = [
        ('Blood', 'Blood'),
        ('Urine', 'Urine'),
        ('Saliva', 'Saliva'),
        ('Swab', 'Swab'),
        ('Other', 'Other'),
    ]

    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    test_name = models.CharField(max_length=150)
    test_code = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='General'
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)

    result_duration = models.CharField(
        max_length=50,
        default='24 hours'
    )

    sample_type = models.CharField(
        max_length=50,
        choices=SAMPLE_TYPE_CHOICES,
        default='Blood'
    )

    description = models.TextField(blank=True)
    preparation_instructions = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    home_collection = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name} ({self.lab.name})"


#Test Booking
class TestBooking(models.Model):

    STATUS_CHOICES = [
        ('Pending Payment', 'Pending Payment'),
        ('Booked', 'Booked'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    booking_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending Payment'
    )
    
    result_file = models.FileField(upload_to='test_results/', null=True, blank=True)
    result_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


#Lab Results
class LabResult(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    lab_technician = models.ForeignKey(LabTechnicianProfile, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=150)
    test_value = models.CharField(max_length=100)
    normal_range = models.CharField(max_length=100)
    result_status = models.CharField(max_length=20)
    remarks = models.TextField()
    test_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Payment(models.Model):

    PAYMENT_METHODS = [
        ('UPI', 'UPI'),
        ('Card', 'Card'),
        ('Cash', 'Cash'),
        ('NetBanking', 'Net Banking'),
    ]

    PAYMENT_STATUS = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]

    patient = models.ForeignKey(
        'PatientProfile',
        on_delete=models.CASCADE,
        related_name="payments"
    )

    appointment = models.ForeignKey(
        'Appointment',
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,      # ✅ IMPORTANT
        blank=True      # ✅ IMPORTANT
    )

    test_booking = models.ForeignKey(
        'TestBooking',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments"
    )


    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def clean(self):
        if not self.appointment and not self.test_booking:
            raise ValidationError(
                "Payment must be linked to either appointment or test booking."
            )

        if self.appointment and self.test_booking  :
            raise ValidationError(
                "Payment cannot be linked to both appointment and test booking."
            )

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4()).replace('-', '').upper()[:12]

        super().save(*args, **kwargs)

        # 🔥 Auto update appointment status when payment is paid
        if self.appointment and self.payment_status == "Paid":
            if self.appointment.status == "Pending Payment":
                self.appointment.status = "Scheduled"
                self.appointment.save()



    def __str__(self):
        return f"{self.patient.full_name} - ₹{self.amount} ({self.payment_status})"


#Login History
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=50)
    device_info = models.CharField(max_length=255)


#Patient Medical 
class PatientHistory(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField()
    recorded_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# These models complement your existing models and should be added to your models.py

class Allergy(models.Model):
    """Patient allergies"""
    SEVERITY_CHOICES = [
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
        ('Critical', 'Critical'),
    ]

    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='allergies')
    name = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    reaction = models.TextField(blank=True, help_text="Describe allergic reactions")
    recorded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-recorded_date']
        unique_together = ('patient', 'name')
        verbose_name_plural = "Allergies"

    def __str__(self):
        return f"{self.patient.full_name} - {self.name} ({self.severity})"


class PatientMedication(models.Model):
    """Patient current medications"""
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='current_medications')
    name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100, blank=True)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg")
    frequency = models.CharField(max_length=100, help_text="e.g., Twice daily")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    prescribing_doctor = models.ForeignKey(
        'DoctorProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    reason = models.TextField(blank=True, help_text="Reason for medication")
    side_effects = models.TextField(blank=True)
    recorded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Current Medications"

    def __str__(self):
        return f"{self.patient.full_name} - {self.name}"

    @property
    def is_active(self):
        """Check if medication is currently active"""
        today = timezone.now().date()
        return self.start_date <= today and (self.end_date is None or self.end_date >= today)


class MedicalCondition(models.Model):
    """Patient medical conditions/chronic diseases"""
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Resolved', 'Resolved'),
    ]

    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='medical_conditions')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    diagnosis_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    icd_code = models.CharField(max_length=20, blank=True, help_text="ICD-10 code")
    severity = models.CharField(
        max_length=20,
        choices=[('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')],
        blank=True
    )
    recorded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-diagnosis_date']
        verbose_name_plural = "Medical Conditions"

    def __str__(self):
        return f"{self.patient.full_name} - {self.name}"


class Surgery(models.Model):
    """Patient surgeries and procedures"""
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='surgeries')
    name = models.CharField(max_length=100)
    date = models.DateField()
    hospital = models.CharField(max_length=100, blank=True)
    surgeon = models.CharField(max_length=100, blank=True)
    anesthesia_type = models.CharField(max_length=100, blank=True)
    complications = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    recorded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.name} ({self.date.year})"


class FamilyHistory(models.Model):
    """Family medical history"""
    RELATION_CHOICES = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Grandfather', 'Grandfather'),
        ('Grandmother', 'Grandmother'),
        ('Aunt', 'Aunt'),
        ('Uncle', 'Uncle'),
        ('Cousin', 'Cousin'),
    ]

    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='family_history')
    relation = models.CharField(max_length=50, choices=RELATION_CHOICES)
    condition = models.CharField(max_length=100)
    age_of_onset = models.IntegerField(null=True, blank=True, help_text="Age when condition started")
    notes = models.TextField(blank=True)
    recorded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_date']
        verbose_name_plural = "Family Histories"

    def __str__(self):
        return f"{self.patient.full_name} - {self.relation}: {self.condition}"


class Immunization(models.Model):
    """Patient immunization records"""
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='immunizations')
    name = models.CharField(max_length=100)
    date = models.DateField()
    vaccine_batch = models.CharField(max_length=50, blank=True)
    administered_by = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    next_due = models.DateField(null=True, blank=True)
    recorded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.name}"

    @property
    def is_overdue(self):
        """Check if next dose is overdue"""
        if self.next_due:
            return self.next_due < timezone.now().date()
        return False


class VitalSigns(models.Model):
    """Patient vital signs records"""
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='vital_signs')
    date = models.DateField()
    time = models.TimeField(default='00:00')
    
    # Cardiovascular
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True, help_text="BPM")
    
    # Body measurements
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="°C")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="cm")
    
    # Respiratory
    respiratory_rate = models.IntegerField(null=True, blank=True, help_text="breaths/min")
    
    # Blood oxygen
    oxygen_saturation = models.IntegerField(null=True, blank=True, help_text="%")
    
    recorded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient.full_name} - Vitals ({self.date})"

    @property
    def bmi(self):
        """Calculate BMI if height and weight are available"""
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 2)
        return None

    @property
    def blood_pressure(self):
        """Return formatted blood pressure"""
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
        return None


class HealthNote(models.Model):
    """General health notes from patient"""
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='health_notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.title}"


class MedicalDocument(models.Model):
    """Medical documents and files"""
    DOCUMENT_TYPE_CHOICES = [
        ('Prescription', 'Prescription'),
        ('Lab Report', 'Lab Report'),
        ('Medical Scan', 'Medical Scan'),
        ('Discharge Summary', 'Discharge Summary'),
        ('Medical Certificate', 'Medical Certificate'),
        ('X-Ray', 'X-Ray'),
        ('MRI', 'MRI'),
        ('CT Scan', 'CT Scan'),
        ('ECG', 'ECG'),
        ('Other', 'Other'),
    ]

    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='medical_documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='medical_documents/')
    date = models.DateField()
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.title}"


class EmergencyContact(models.Model):
    """Patient emergency contacts"""
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary']

    def __str__(self):
        return f"{self.patient.full_name} - {self.name} ({self.relationship})"


class BloodDonationHistory(models.Model):
    """Patient blood donation records"""
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, related_name='blood_donations')
    donation_date = models.DateField()
    blood_bank = models.CharField(max_length=100, blank=True)
    blood_quantity = models.IntegerField(help_text="in ml")
    next_eligible_date = models.DateField()
    notes = models.TextField(blank=True)
    recorded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-donation_date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.donation_date}"

# Create your models here.

from django.db import models
from django.core.exceptions import ValidationError


class DoctorAvailability(models.Model):
    doctor = models.OneToOneField(
        'DoctorProfile',
        on_delete=models.CASCADE,
        related_name='availability'
    )

    working_days = models.CharField(
        max_length=100,
        help_text="Comma-separated values (e.g., Mon,Tue,Wed)"
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)

    slot_duration = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )

    max_appointments = models.PositiveIntegerField(
        default=10
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validate time logic
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

        if self.break_start and self.break_end:
            if self.break_start >= self.break_end:
                raise ValidationError("Break end must be after break start.")

            if not (self.start_time <= self.break_start <= self.end_time):
                raise ValidationError("Break must be within working hours.")

    def __str__(self):
        return f"{self.doctor} Availability"
