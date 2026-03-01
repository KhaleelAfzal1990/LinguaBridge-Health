from django.urls import path
from . import views

urlpatterns = [
    # Session management
    path('sessions/', views.ClinicalSessionListView.as_view(), name='session-list'),
    path('sessions/<int:pk>/', views.ClinicalSessionDetailView.as_view(), name='session-detail'),
    
    # Processing
    path('process/', views.ProcessNarrativeView.as_view(), name='process-narrative'),
    path('detect-idioms/', views.DetectIdiomsOnlyView.as_view(), name='detect-idioms'),
    path('sessions/<int:session_id>/soap/', views.GenerateSOAPNoteView.as_view(), name='generate-soap'),
    
    # Idiom and medical data
    path('idioms/', views.PatientIdiomListView.as_view(), name='idiom-list'),
    path('systems/', views.MedicalSystemListView.as_view(), name='medical-system-list'),
    path('specialties/', views.MedicalSpecialtyListView.as_view(), name='medical-specialty-list'),
]