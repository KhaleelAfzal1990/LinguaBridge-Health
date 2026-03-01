import logging
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import (
    ClinicalSession, ClinicalSummary, IntakeResponse, 
    IdiomMapping, 
   # IdiomDetectionResult, 
    MedicalSystem, MedicalSpecialty
)
from .serializers import (
    ClinicalSessionSerializer, ClinicalSessionCreateSerializer,
    PatientIdiomSerializer, MedicalSystemSerializer, MedicalSpecialtySerializer,
    IntakeResponseSerializer, ClinicalSummarySerializer,
    ProcessNarrativeSerializer
)
from .ai_processor import ClinicalAIProcessor, IdiomDetector
from linguabridge.apps.accounts.models import PatientProfile, DoctorProfile
from .models import PatientIdiom
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

logger = logging.getLogger(__name__)

class ProcessNarrativeView(APIView):
    """
    Process patient narrative (text or audio) and return structured clinical data
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ProcessNarrativeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        text = data.get('text', '')
        audio_file = data.get('audio_file')
        session_id = data.get('session_id')
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        context = data.get('context', {})
        
        # Get or create session
        if session_id:
            session = get_object_or_404(ClinicalSession, id=session_id)
        else:
            patient = get_object_or_404(PatientProfile, id=patient_id)
            doctor = get_object_or_404(DoctorProfile, id=doctor_id)
            session = ClinicalSession.objects.create(
                patient=patient,
                doctor=doctor,
                status='processing'
            )
        
        # Process audio if provided
        if audio_file and not text:
            text = self._transcribe_audio(audio_file)
            session.audio_file = audio_file
            session.raw_transcript = text
            session.save()
        
        # Detect idioms first
        idiom_detector = IdiomDetector()
        detected_idioms = idiom_detector.detect_idioms(text)
        
        # Save detected idioms to session
        session.detected_idioms = detected_idioms
        
        # Extract risk flags
        risk_flags = list(set([d['risk_note'] for d in detected_idioms if d.get('risk_note')]))
        session.risk_flags = risk_flags
        session.save()
        
        # Save individual idiom detections
        for det in detected_idioms:
            #idiom = PatientIdiom.objects.get(idiom=det['idiom'])
            idiom = IdiomMapping.objects.get(idiom=det['idiom'])
            # IdiomDetectionResult.objects.create(
            #     session=session,
            #     idiom=idiom,
            #     matched_text=det['matched_text'],
            #     position_start=det.get('position_start'),
            #     position_end=det.get('position_end'),
            #     confidence=det['confidence']
            # )
        
        # Add idiom context for AI
        context['detected_idioms'] = detected_idioms
        context['risk_flags'] = risk_flags
        
        # Process with AI
        try:
            ai_processor = ClinicalAIProcessor(provider=request.GET.get('provider', None))
            clinical_data = ai_processor.process_patient_narrative(text, context)
            
            # Add confidence score and update session
            session.processed_data = clinical_data
            session.confidence_score = clinical_data.get('confidence_score', 0.0)
            session.ai_provider_used = ai_processor.provider
            session.status = 'completed'
            session.save()
            
            # Create intake responses for follow-up questions
            if 'suggested_follow_up_questions' in clinical_data:
                for question in clinical_data.get('suggested_follow_up_questions', []):
                    IntakeResponse.objects.create(
                        session=session,
                        question=question,
                        response_text=''  # Will be filled in follow-up
                    )
            
            # Generate explanation
            explanation = ai_processor.explain_transformation(
                text, 
                clinical_data, 
                detected_idioms
            )
            
            # Create or update summary
            summary, created = ClinicalSummary.objects.update_or_create(
                session=session,
                defaults={
                    'summary_type': 'chief_complaint',
                    'content': clinical_data,
                    'explanation': explanation,
                    'risk_warnings': risk_flags
                }
            )
            
            return Response({
                'session_id': session.id,
                'clinical_data': clinical_data,
                'explanation': explanation,
                'idioms_detected': detected_idioms,
                'risk_flags': risk_flags,
                'confidence_score': session.confidence_score,
                'summary': ClinicalSummarySerializer(summary).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            session.status = 'failed'
            session.save()
            logger.error(f"Processing failed for session {session.id}: {str(e)}")
            return Response({
                'error': 'Processing failed',
                'detail': str(e),
                'idioms_detected': detected_idioms,  # Still return idiom detections
                'risk_flags': risk_flags
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _transcribe_audio(self, audio_file):
        """Transcribe audio file to text"""
        recognizer = sr.Recognizer()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            for chunk in audio_file.chunks():
                tmp_file.write(chunk)
            tmp_path = tmp_file.name
        
        try:
            audio = AudioSegment.from_file(tmp_path)
            audio.export(tmp_path, format='wav')
            
            with sr.AudioFile(tmp_path) as source:
                audio_data = recognizer.record(source)
                # Try multiple languages
                try:
                    text = recognizer.recognize_google(audio_data, language='ur-PK')
                except:
                    try:
                        text = recognizer.recognize_google(audio_data, language='en-US')
                    except:
                        text = recognizer.recognize_google(audio_data, language='ur-PK,en-US')
            
            return text
            
        finally:
            os.unlink(tmp_path)

# New views for managing idioms
class PatientIdiomListView(generics.ListAPIView):
    """List all patient idioms with their clinical mappings"""
    queryset = PatientIdiom.objects.filter(is_active=True)
    serializer_class = PatientIdiomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['idiom', 'clinical_terms__term', 'risk_note']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by system
        system = self.request.query_params.get('system')
        if system:
            queryset = queryset.filter(primary_system__name__iexact=system)
        
        # Filter by specialty
        specialty = self.request.query_params.get('specialty')
        if specialty:
            queryset = queryset.filter(primary_specialty__name__iexact=specialty)
        
        return queryset

class MedicalSystemListView(generics.ListAPIView):
    """List all medical systems"""
    queryset = MedicalSystem.objects.all()
    serializer_class = MedicalSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicalSpecialtyListView(generics.ListAPIView):
    """List all medical specialties"""
    queryset = MedicalSpecialty.objects.all()
    serializer_class = MedicalSpecialtySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        system_id = self.request.query_params.get('system')
        if system_id:
            queryset = queryset.filter(system_id=system_id)
        return queryset
class ClinicalSessionListView(generics.ListAPIView):
    queryset = ClinicalSession.objects.all()
    serializer_class = ClinicalSessionSerializer
class ClinicalSessionDetailView(generics.RetrieveAPIView):
    queryset = ClinicalSession.objects.all()
    serializer_class = ClinicalSessionSerializer
class GenerateSOAPNoteView(APIView):

    def post(self, request, session_id):
        try:
            session = ClinicalSession.objects.get(id=session_id)
        except ClinicalSession.DoesNotExist:
            return Response(
                {"error": "Session not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Placeholder logic (replace with your AI logic later)
        soap_note = {
            "subjective": "Patient reports improvement.",
            "objective": "Vitals stable.",
            "assessment": "Stable condition.",
            "plan": "Continue medication."
        }

        return Response(soap_note, status=status.HTTP_200_OK)
class DetectIdiomsOnlyView(APIView):
    """
    Only detect idioms without full AI processing
    Useful for quick checks or pre-processing
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        detector = IdiomDetector()
        detected = detector.detect_idioms(text)
        context = detector.extract_clinical_context(text)
        
        return Response({
            'detected_idioms': detected,
            'systems_involved': context['systems'],
            'specialties_involved': context['specialties'],
            'possible_conditions': context['possible_conditions'],
            'risk_flags': context['risk_flags']
        })