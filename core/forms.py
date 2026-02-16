from django import forms

class LabTechnicianForm(forms.Form):
    # Account info
    username = forms.CharField(
        max_length=150,
        label="Username"
    )

    email = forms.EmailField(
        label="Email Address"
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    # Personal info
    first_name = forms.CharField(
        max_length=100,
        label="First Name"
    )

    last_name = forms.CharField(
        max_length=100,
        label="Last Name"
    )

    phone = forms.CharField(
        max_length=15,
        label="Phone Number"
    )

    status = forms.ChoiceField(
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive')
        ],
        label="Status"
    )

    # Lab assignment (optional)
    lab_id = forms.IntegerField(
        required=False,
        label="Assign Lab"
    )

    # Additional info
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Experience, certifications, skills...'
        }),
        label="Bio / About"
    )

    # 🔐 Password validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")

        return cleaned_data

# forms.py - Patient Appointment Reschedule Forms

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment, DoctorProfile


class RescheduleAppointmentForm(forms.ModelForm):
    """
    Form for rescheduling an appointment
    """
    doctor = forms.ModelChoiceField(
        queryset=DoctorProfile.objects.filter(status='Active'),  # ✅ FIXED: Using DoctorProfile and filtering by status
        required=True,
        widget=forms.RadioSelect,
        label='Select Doctor'
    )
    
    appointment_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input',
            'min': (timezone.now().date() + timedelta(days=1)).strftime('%Y-%m-%d')
        }),
        label='Appointment Date'
    )
    
    appointment_time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-input'
        }),
        label='Appointment Time'
    )
    
    reschedule_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 3,
            'placeholder': 'Please let us know why you need to reschedule...'
        }),
        label='Reason for Rescheduling'
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 3,
            'placeholder': 'Any additional notes or concerns for your appointment...'
        }),
        label='Notes for the Doctor'
    )
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If we have an instance, set the current doctor as selected
        if self.instance and self.instance.pk:
            self.fields['doctor'].initial = self.instance.doctor
    
    def clean_appointment_date(self):
        """
        Validate that the appointment date is in the future
        """
        appointment_date = self.cleaned_data.get('appointment_date')
        
        if not appointment_date:
            raise ValidationError('Please select an appointment date.')
        
        # Must be at least 1 day in the future
        min_date = timezone.now().date() + timedelta(days=1)
        
        if appointment_date < min_date:
            raise ValidationError(
                'Appointments must be scheduled at least 24 hours in advance.'
            )
        
        # Optional: Don't allow appointments too far in the future (e.g., 3 months)
        max_date = timezone.now().date() + timedelta(days=90)
        
        if appointment_date > max_date:
            raise ValidationError(
                'Appointments cannot be scheduled more than 3 months in advance.'
            )
        
        return appointment_date
    
    def clean_appointment_time(self):
        """
        Validate that the appointment time is within working hours
        """
        appointment_time = self.cleaned_data.get('appointment_time')
        
        if not appointment_time:
            raise ValidationError('Please select an appointment time.')
        
        # Define working hours (9 AM to 6 PM)
        opening_time = datetime.strptime('09:00', '%H:%M').time()
        closing_time = datetime.strptime('18:00', '%H:%M').time()
        
        if appointment_time < opening_time or appointment_time > closing_time:
            raise ValidationError(
                'Appointments must be between 9:00 AM and 6:00 PM.'
            )
        
        return appointment_time
    
    def clean(self):
        """
        Validate that the appointment datetime is in the future
        and check for conflicts
        """
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        doctor = cleaned_data.get('doctor')
        
        if appointment_date and appointment_time:
            # Check if the datetime is in the future
            appointment_datetime = datetime.combine(
                appointment_date, 
                appointment_time
            )
            
            # Make timezone aware if your project uses timezones
            if timezone.is_aware(timezone.now()):
                appointment_datetime = timezone.make_aware(appointment_datetime)
            
            if appointment_datetime <= timezone.now():
                raise ValidationError(
                    'The appointment date and time must be in the future.'
                )
            
            # Check if the slot is available (if doctor is selected)
            if doctor:
                # Exclude current appointment when checking conflicts
                exclude_id = self.instance.pk if self.instance else None
                
                conflicting_appointments = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    status__in=['Pending Payment', 'Scheduled', 'Confirmed']  # ✅ Updated to match your STATUS_CHOICES
                )
                
                if exclude_id:
                    conflicting_appointments = conflicting_appointments.exclude(id=exclude_id)
                
                if conflicting_appointments.exists():
                    raise ValidationError(
                        'This time slot is already booked. Please select another time.'
                    )
        
        return cleaned_data


class CancelAppointmentForm(forms.Form):
    """
    Simple form for appointment cancellation with optional reason
    """
    cancellation_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 4,
            'placeholder': 'Please let us know why you need to cancel (optional)...'
        }),
        label='Reason for Cancellation'
    )
    
    confirm_cancellation = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox'
        }),
        label='I confirm that I want to cancel this appointment'
    )