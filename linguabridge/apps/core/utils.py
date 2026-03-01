import hashlib
import hmac
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random
import string

def generate_otp(length=6):
    """Generate numeric OTP"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp):
    """Send OTP via email"""
    subject = 'Your LinguaBridge Health Verification Code'
    message = f'Your verification code is: {otp}'
    html_message = render_to_string('emails/otp.html', {'otp': otp, 'expiry': 10})
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=html_message,
        fail_silently=False,
    )

def send_sms(phone_number, message):
    """Send SMS (implement with your SMS provider)"""
    # Integrate with Twilio, Nexmo, or local provider
    pass

def calculate_age(birth_date):
    """Calculate age from birth date"""
    today = datetime.now().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def sanitize_phone_number(phone):
    """Sanitize phone number to international format"""
    # Remove all non-digit characters
    phone = ''.join(filter(str.isdigit, phone))
    
    # Handle Pakistan numbers
    if phone.startswith('0'):
        phone = '92' + phone[1:]
    elif not phone.startswith('92'):
        phone = '92' + phone
    
    return phone

def create_webhook_signature(payload, secret=None):
    """Create HMAC signature for webhook payload"""
    secret = secret or settings.WEBHOOK_SECRET
    payload_bytes = json.dumps(payload).encode('utf-8')
    signature = hmac.new(
        secret.encode('utf-8'),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_webhook_signature(payload, signature, secret=None):
    """Verify webhook signature"""
    expected = create_webhook_signature(payload, secret)
    return hmac.compare_digest(expected, signature)

def format_clinical_text(text, max_length=500):
    """Format clinical text for display"""
    if len(text) <= max_length:
        return text
    
    # Try to cut at sentence boundary
    sentences = text.split('. ')
    result = ''
    for sentence in sentences:
        if len(result) + len(sentence) + 2 <= max_length:
            result += sentence + '. '
        else:
            break
    
    return result.strip() + '...'

class ClinicalScoreCalculator:
    """Calculate various clinical scores"""
    
    @staticmethod
    def calculate_news_score(vital_signs):
        """
        Calculate National Early Warning Score (NEWS)
        vital_signs: dict with keys - respiration_rate, oxygen_saturation, 
                     systolic_bp, heart_rate, consciousness, temperature
        """
        score = 0
        
        # Respiration rate
        rr = vital_signs.get('respiration_rate', 0)
        if rr <= 8 or rr >= 25:
            score += 3
        elif rr >= 21:
            score += 2
        elif rr >= 12:
            score += 0
        else:
            score += 1
        
        # Oxygen saturation
        spo2 = vital_signs.get('oxygen_saturation', 0)
        if spo2 <= 91:
            score += 3
        elif spo2 <= 93:
            score += 2
        elif spo2 <= 95:
            score += 1
        
        # Temperature
        temp = vital_signs.get('temperature', 0)
        if temp <= 35.0:
            score += 3
        elif temp >= 39.1:
            score += 2
        elif temp >= 38.1:
            score += 1
        elif temp >= 36.1:
            score += 0
        
        return score
    
    @staticmethod
    def assess_urgency(clinical_data):
        """Assess urgency based on clinical data"""
        score = 0
        
        # Check for red flags in symptoms
        red_flags = [
            'chest pain', 'shortness of breath', 'unconscious',
            'bleeding', 'severe pain', 'paralysis'
        ]
        
        chief_complaint = clinical_data.get('chief_complaint', '').lower()
        for flag in red_flags:
            if flag in chief_complaint:
                score += 5
        
        severity = clinical_data.get('severity', 0)
        if severity >= 8:
            score += 3
        elif severity >= 5:
            score += 1
        
        if score >= 5:
            return 'emergency'
        elif score >= 3:
            return 'urgent'
        else:
            return 'routine'