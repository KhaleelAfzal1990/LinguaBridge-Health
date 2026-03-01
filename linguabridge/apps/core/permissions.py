from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    """Allow access only to doctors"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'doctor'

class IsPatient(permissions.BasePermission):
    """Allow access only to patients"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'patient'

class IsClinicAdmin(permissions.BasePermission):
    """Allow access only to clinic admins"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'clinic_admin'

class IsOwnerOrDoctor(permissions.BasePermission):
    """Object-level permission to allow owners or doctors to edit"""
    
    def has_object_permission(self, request, view, obj):
        # Doctors can access all
        if request.user.user_type == 'doctor':
            return True
        
        # Check if user is the patient
        if hasattr(obj, 'patient'):
            return obj.patient.user == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False

class CanAccessClinicalData(permissions.BasePermission):
    """Check if user can access clinical data"""
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Doctors can access their patients' data
        if user.user_type == 'doctor':
            if hasattr(obj, 'doctor'):
                return obj.doctor.user == user
            elif hasattr(obj, 'session') and hasattr(obj.session, 'doctor'):
                return obj.session.doctor.user == user
        
        # Patients can access their own data
        elif user.user_type == 'patient':
            if hasattr(obj, 'patient'):
                return obj.patient.user == user
            elif hasattr(obj, 'session') and hasattr(obj.session, 'patient'):
                return obj.session.patient.user == user
        
        return False