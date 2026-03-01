from django.db import models
from django.conf import settings
# Use string references instead of direct imports to avoid circular imports
# from apps.accounts.models import DoctorProfile, PatientProfile, Clinic
# from apps.clinical_intake.models import ClinicalSession

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    # Use string references for ForeignKey to avoid circular imports
    patient = models.ForeignKey('accounts.PatientProfile', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('accounts.DoctorProfile', on_delete=models.CASCADE, related_name='appointments')
    clinic = models.ForeignKey('accounts.Clinic', on_delete=models.CASCADE, related_name='appointments', null=True)
    clinical_session = models.OneToOneField('clinical_intake.ClinicalSession', on_delete=models.SET_NULL, null=True, blank=True)
    
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration_minutes = models.IntegerField(default=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

class Consultation(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='consultation')
    clinical_session = models.OneToOneField('clinical_intake.ClinicalSession', on_delete=models.CASCADE, related_name='consultation')
    
    vital_signs = models.JSONField(default=dict)  # {'bp': '120/80', 'hr': 72, 'temp': 98.6}
    physical_exam = models.TextField(blank=True)
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    prescriptions = models.JSONField(default=list)  # List of prescribed medications
    lab_orders = models.JSONField(default=list)  # List of ordered tests
    follow_up_date = models.DateField(null=True, blank=True)
    doctor_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Prescription(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='prescription_list')
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    refills = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

class Referral(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='referrals')
    referred_to = models.ForeignKey('accounts.DoctorProfile', on_delete=models.CASCADE, related_name='referrals_received')
    reason = models.TextField()
    urgency = models.CharField(max_length=20, choices=(
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    ))
    summary = models.JSONField(default=dict)  # Referral summary from clinical session
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('declined', 'Declined'),
    ), default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)