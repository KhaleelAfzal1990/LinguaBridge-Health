from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.UserDetailView.as_view(), name='user-detail'),
    path('doctor/profile/', views.DoctorProfileView.as_view(), name='doctor-profile'),
    path('patient/profile/', views.PatientProfileView.as_view(), name='patient-profile'),
    path('clinics/', views.ClinicListView.as_view(), name='clinic-list'),
    path('clinics/<int:pk>/', views.ClinicDetailView.as_view(), name='clinic-detail'),
]