from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/<int:appointment_id>/start/', views.StartConsultationView.as_view(), name='start-consultation'),
    path('consultations/<int:pk>/', views.ConsultationDetailView.as_view(), name='consultation-detail'),
    path('consultations/<int:consultation_id>/prescriptions/', views.AddPrescriptionView.as_view(), name='add-prescription'),
    path('consultations/<int:consultation_id>/referrals/', views.GenerateReferralView.as_view(), name='generate-referral'),
    path('consultations/<int:consultation_id>/complete/', views.CompleteConsultationView.as_view(), name='complete-consultation'),
]