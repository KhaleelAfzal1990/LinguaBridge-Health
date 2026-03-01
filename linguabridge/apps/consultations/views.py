from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from .models import Appointment, Consultation, Prescription, Referral
from .serializers import AppointmentSerializer, ConsultationSerializer, PrescriptionSerializer, ReferralSerializer
from linguabridge.apps.clinical_intake.models import ClinicalSession
from linguabridge.apps.clinical_intake.ai_processor import ClinicalAIProcessor

class AppointmentListView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Appointment.objects.all()

        # Filter by user type safely
        if getattr(user, 'user_type', None) == 'doctor' and hasattr(user, 'doctor_profile'):
            queryset = queryset.filter(doctor=user.doctor_profile)
        elif getattr(user, 'user_type', None) == 'patient' and hasattr(user, 'patient_profile'):
            queryset = queryset.filter(patient=user.patient_profile)
        else:
            # User has no profile or unknown type
            return Appointment.objects.none()

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        date_format = "%Y-%m-%d"
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, date_format)
                queryset = queryset.filter(appointment_date__gte=start_date_obj)
            except ValueError:
                pass
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, date_format)
                queryset = queryset.filter(appointment_date__lte=end_date_obj)
            except ValueError:
                pass

        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        return queryset


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class StartConsultationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)

        if hasattr(appointment, 'consultation'):
            return Response({'error': 'Consultation already started'}, status=status.HTTP_400_BAD_REQUEST)

        # Create clinical session if not exists
        clinical_session = appointment.clinical_session
        if not clinical_session:
            clinical_session = ClinicalSession.objects.create(
                patient=getattr(appointment, 'patient', None),
                doctor=getattr(appointment, 'doctor', None),
                status='pending'
            )
            appointment.clinical_session = clinical_session
            appointment.save()

        consultation = Consultation.objects.create(
            appointment=appointment,
            clinical_session=clinical_session
        )

        appointment.status = 'in_progress'
        appointment.save()

        return Response({
            'consultation': ConsultationSerializer(consultation).data,
            'clinical_session_id': clinical_session.id
        }, status=status.HTTP_201_CREATED)


class ConsultationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]


class AddPrescriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, consultation_id):
        consultation = get_object_or_404(Consultation, id=consultation_id)
        serializer = PrescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prescription = serializer.save(consultation=consultation)
        return Response(PrescriptionSerializer(prescription).data, status=status.HTTP_201_CREATED)


class GenerateReferralView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, consultation_id):
        consultation = get_object_or_404(Consultation, id=consultation_id)

        if not getattr(consultation.clinical_session, 'processed_data', None):
            return Response({'error': 'Clinical session not processed'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ai_processor = ClinicalAIProcessor()
            patient = consultation.appointment.patient.user if consultation.appointment.patient else None

            referral_data = {
                'patient_info': {
                    'name': patient.get_full_name() if patient else '',
                    'age': getattr(patient, 'date_of_birth', None),
                    'contact': getattr(patient, 'phone_number', '')
                },
                'clinical_data': consultation.clinical_session.processed_data,
                'diagnosis': consultation.diagnosis,
                'reason_for_referral': request.data.get('reason', ''),
                'urgency': request.data.get('urgency', 'routine')
            }

            referral = Referral.objects.create(
                consultation=consultation,
                referred_to_id=request.data.get('referred_to'),
                reason=request.data.get('reason', ''),
                urgency=request.data.get('urgency', 'routine'),
                summary=referral_data
            )

            return Response(ReferralSerializer(referral).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompleteConsultationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, consultation_id):
        consultation = get_object_or_404(Consultation, id=consultation_id)

        consultation.diagnosis = request.data.get('diagnosis', consultation.diagnosis)
        consultation.treatment_plan = request.data.get('treatment_plan', consultation.treatment_plan)
        consultation.doctor_notes = request.data.get('doctor_notes', consultation.doctor_notes)
        consultation.vital_signs = request.data.get('vital_signs', consultation.vital_signs)
        consultation.physical_exam = request.data.get('physical_exam', consultation.physical_exam)
        consultation.follow_up_date = request.data.get('follow_up_date')
        consultation.save()

        # Update appointment status
        if consultation.appointment:
            consultation.appointment.status = 'completed'
            consultation.appointment.save()

        # Update clinical session status
        if consultation.clinical_session:
            consultation.clinical_session.status = 'completed'
            consultation.clinical_session.save()

        return Response(ConsultationSerializer(consultation).data)