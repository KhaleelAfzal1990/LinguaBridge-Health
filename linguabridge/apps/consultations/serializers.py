from rest_framework import serializers
from .models import Appointment, Consultation, Prescription, Referral
from linguabridge.apps.accounts.serializers import DoctorProfileSerializer, PatientProfileSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    patient_details = PatientProfileSerializer(source='patient', read_only=True)
    doctor_details = DoctorProfileSerializer(source='doctor', read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    appointment_details = AppointmentSerializer(source='appointment', read_only=True)
    
    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')