from rest_framework import serializers
# from .models import (
#     ClinicalSession, 
#     #PatientIdiom,
#      #MedicalSystem, MedicalSpecialty, 
#     ClinicalTerm, IntakeResponse, ClinicalSummary, IdiomDetectionResult
# )
from .models import (
    ClinicalSession, ClinicalSummary, IntakeResponse, 
    IdiomMapping
    , ClinicalTerm,
   IdiomDetectionResult, 
   MedicalSystem, MedicalSpecialty
)

class MedicalSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalSystem
        fields = ['id', 'name', 'description', 'created_at']

class MedicalSpecialtySerializer(serializers.ModelSerializer):
    system_name = serializers.CharField(source='system.name', read_only=True)
    
    class Meta:
        model = MedicalSpecialty
        # fields = ['id', 'name', 'system', 'system_name', 'description', 'created_at']
        fields = ['id', 'name', 'system_name', 'description', 'created_at']

class ClinicalTermSerializer(serializers.ModelSerializer):
    system_name = serializers.CharField(source='system.name', read_only=True)
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    
    class Meta:
        model = ClinicalTerm
        # fields = ['id', 'term', 'full_form', 'description', 'system', 'system_name', 
        #          'specialty', 'specialty_name', 'created_at']
        fields = ['id', 'term',  'description', 'system_name', 
                 'specialty_name', 'created_at']

class PatientIdiomSerializer(serializers.ModelSerializer):
    clinical_terms = ClinicalTermSerializer(many=True, read_only=True)
    clinical_term_ids = serializers.PrimaryKeyRelatedField(
        queryset=ClinicalTerm.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='clinical_terms'
    )

    class Meta:
        model = IdiomMapping
        fields = '__all__'
        
class IdiomDetectionResultSerializer(serializers.ModelSerializer):
    idiom_text = serializers.CharField(source='idiom.idiom', read_only=True)
    clinical_terms = serializers.SerializerMethodField()
    risk_note = serializers.CharField(source='idiom.risk_note', read_only=True)
    
    class Meta:
        model = IdiomDetectionResult
        # fields = ['id', 'idiom', 'idiom_text', 'clinical_terms', 'risk_note',
        #          'matched_text', 'position_start', 'position_end', 
        #          'confidence', 'created_at']
        fields = ['id', 'idiom_text', 'clinical_terms', 'risk_note',
                 'matched_text',  
                  'created_at']
    
    def get_clinical_terms(self, obj):
        return [term.term for term in obj.idiom.clinical_terms.all()]

class ClinicalSessionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    idiom_detections = IdiomDetectionResultSerializer(many=True, read_only=True)
    
    class Meta:
        model = ClinicalSession
        # fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name',
        #          'session_date', 'status', 'audio_file', 'audio_duration',
        #          'raw_transcript', 'processed_data', 'detected_idioms',
        #          'risk_flags', 'idiom_detections', 'ai_provider_used',
        #          'confidence_score', 'created_at', 'updated_at']
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name',
                 'session_date', 'status', 'audio_file', 'audio_duration',
                 'raw_transcript', 'processed_data',
                'idiom_detections', 'ai_provider_used',
                 'confidence_score', 'created_at', 'updated_at']

        read_only_fields = ['created_at', 'updated_at']

class ClinicalSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalSession
        fields = ['id', 'patient', 'doctor', 'audio_file', 'audio_duration']

class IntakeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntakeResponse
        fields = '__all__'
        read_only_fields = ['created_at']

class ClinicalSummarySerializer(serializers.ModelSerializer):
    session_info = ClinicalSessionSerializer(source='session', read_only=True)
    
    class Meta:
        model = ClinicalSummary
        fields = ['id', 'session', 'session_info', 'summary_type', 'content',
                 'explanation', 'risk_warnings', 'doctor_approved',
                 'doctor_notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProcessNarrativeSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, help_text="Patient's narrative text")
    audio_file = serializers.FileField(required=False, help_text="Audio recording of patient")
    session_id = serializers.IntegerField(required=False, help_text="Existing session ID if continuing")
    patient_id = serializers.IntegerField(required=True)
    doctor_id = serializers.IntegerField(required=True)
    context = serializers.JSONField(required=False, default=dict)
    
    def validate(self, data):
        if not data.get('text') and not data.get('audio_file'):
            raise serializers.ValidationError("Either text or audio_file must be provided")
        return data