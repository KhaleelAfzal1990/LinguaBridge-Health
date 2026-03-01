import openai
import json
import logging
import re
from typing import Dict, Any, Optional, List, Tuple
from django.conf import settings
from django.core.cache import cache
import anthropic
# import google.generativeai as genai
from google import genai
from dataclasses import dataclass
from .models import PatientIdiom, ClinicalTerm, MedicalSystem, MedicalSpecialty

logger = logging.getLogger(__name__)

@dataclass
class AIProvider:
    name: str
    api_key: str
    model: str
    temperature: float = 0.3
    max_tokens: int = 2000

class IdiomDetector:
    """
    Detect and map patient idioms to clinical terms using the database
    """
    
    def __init__(self):
        self.idiom_cache = {}
        self._load_idioms()
    
    def _load_idioms(self):
        """Load all idioms from database into cache"""
        # Try to get from cache first
        cached = cache.get('all_idioms')
        if cached:
            self.idiom_cache = cached
            return
        
        # Load from database
        idioms = PatientIdiom.objects.filter(is_active=True).select_related(
            'primary_system', 'primary_specialty'
        ).prefetch_related('clinical_terms')
        
        for idiom in idioms:
            self.idiom_cache[idiom.idiom.lower()] = {
                'id': idiom.id,
                'idiom': idiom.idiom,
                'clinical_terms': [term.term for term in idiom.clinical_terms.all()],
                'system': idiom.primary_system.name if idiom.primary_system else None,
                'specialty': idiom.primary_specialty.name if idiom.primary_specialty else None,
                'risk_note': idiom.risk_note,
                'confidence_weight': idiom.confidence_weight
            }
        
        # Cache for 1 hour
        cache.set('all_idioms', self.idiom_cache, 3600)
    
    def detect_idioms(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect idioms in text and return clinical mappings
        
        Args:
            text: Patient's narrative text
            
        Returns:
            List of detected idioms with clinical mappings
        """
        text_lower = text.lower()
        detected = []
        
        # Sort idioms by length (longest first) to prioritize more specific matches
        sorted_idioms = sorted(self.idiom_cache.items(), key=lambda x: len(x[0]), reverse=True)
        
        for idiom_lower, mapping in sorted_idioms:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(idiom_lower) + r'\b'
            matches = list(re.finditer(pattern, text_lower))
            
            for match in matches:
                detected.append({
                    'idiom': mapping['idiom'],
                    'matched_text': match.group(),
                    'position_start': match.start(),
                    'position_end': match.end(),
                    'clinical_terms': mapping['clinical_terms'],
                    'system': mapping['system'],
                    'specialty': mapping['specialty'],
                    'risk_note': mapping['risk_note'],
                    'confidence': mapping['confidence_weight']
                })
        
        return detected
    
    def extract_clinical_context(self, text: str) -> Dict[str, Any]:
        """
        Extract clinical context from text based on detected idioms
        
        Returns:
            Dictionary with systems involved, possible conditions, and risk flags
        """
        detected = self.detect_idioms(text)
        
        if not detected:
            return {
                'systems': [],
                'possible_conditions': [],
                'risk_flags': [],
                'specialties': []
            }
        
        # Aggregate systems and conditions
        systems = set()
        specialties = set()
        possible_conditions = set()
        risk_flags = []
        
        for item in detected:
            if item['system']:
                systems.add(item['system'])
            if item['specialty']:
                specialties.add(item['specialty'])
            if item['risk_note'] and item['risk_note'] not in risk_flags:
                risk_flags.append(item['risk_note'])
            for term in item['clinical_terms']:
                possible_conditions.add(term)
        
        return {
            'systems': list(systems),
            'specialties': list(specialties),
            'possible_conditions': list(possible_conditions),
            'risk_flags': risk_flags,
            'detections': detected
        }

class ClinicalAIProcessor:
    """
    Handles all AI processing for clinical intake with support for multiple providers
    """
    
    def __init__(self, provider: str = None):
        self.provider = provider or settings.DEFAULT_AI_PROVIDER
        self.idiom_detector = IdiomDetector()
        self._setup_provider()
        
    def _setup_provider(self):
        """Setup the AI provider based on configuration"""
        if self.provider == 'openai':
            openai.api_key = settings.OPENAI_API_KEY
            self.client = openai
            self.model = "gpt-4"
            
        elif self.provider == 'deepseek':
            self.client = openai
            self.client.api_key = settings.DEEPSEEK_API_KEY
            self.client.api_base = "https://api.deepseek.com/v1"
            self.model = "deepseek-chat"
            
        elif self.provider == 'anthropic':
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = "claude-3-opus-20240229"
            
        elif self.provider == 'gemini':
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.client = genai
            self.model = "gemini-pro"
    
    def process_patient_narrative(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process patient narrative in Urdu-English mix and return structured clinical data
        
        First detects idioms from database, then enhances with AI
        """
        # First, detect idioms from our database
        idiom_context = self.idiom_detector.extract_clinical_context(text)
        
        # Build prompt with detected idioms as context
        prompt = self._build_clinical_extraction_prompt(text, context, idiom_context)
        
        try:
            if self.provider in ['openai', 'deepseek']:
                response = self._call_openai_compatible(prompt)
            elif self.provider == 'anthropic':
                response = self._call_anthropic(prompt)
            elif self.provider == 'gemini':
                response = self._call_gemini(prompt)
            
            clinical_data = self._parse_clinical_response(response)
            
            # Add idiom detection results to clinical data
            clinical_data['detected_idioms'] = idiom_context['detections']
            clinical_data['risk_flags'] = idiom_context['risk_flags']
            clinical_data['systems_involved'] = idiom_context['systems']
            clinical_data['possible_conditions'] = idiom_context['possible_conditions']
            
            return clinical_data
            
        except Exception as e:
            logger.error(f"AI processing failed: {str(e)}")
            # Return at least the idiom detection results
            return {
                'error': str(e),
                'detected_idioms': idiom_context['detections'],
                'risk_flags': idiom_context['risk_flags'],
                'systems_involved': idiom_context['systems'],
                'possible_conditions': idiom_context['possible_conditions'],
                'confidence_score': 0.5
            }
    
    def _build_clinical_extraction_prompt(self, text: str, context: Optional[Dict], idiom_context: Dict) -> str:
        """Build prompt with idiom context from database"""
        
        # Format detected idioms for the prompt
        idiom_summary = ""
        if idiom_context['detections']:
            idiom_summary = "Detected patient expressions with clinical mappings:\n"
            for det in idiom_context['detections']:
                idiom_summary += f"- '{det['idiom']}' → {', '.join(det['clinical_terms'])}"
                if det['risk_note']:
                    idiom_summary += f" (⚠️ {det['risk_note']})"
                idiom_summary += "\n"
        
        context_str = ""
        if context:
            context_str = f"""
            Patient Context:
            - Age: {context.get('age', 'Unknown')}
            - Gender: {context.get('gender', 'Unknown')}
            - Known conditions: {context.get('conditions', 'None')}
            - Current medications: {context.get('medications', 'None')}
            """
        
        prompt = f"""
        You are LinguaBridge Health, an AI clinical intake system specialized in understanding 
        Urdu-English mixed patient narratives from South Asia. Your task is to extract structured 
        clinical information from the patient's words.
        
        {context_str}
        
        {idiom_summary}
        
        Patient's Narrative:
        "{text}"
        
        Please analyze this narrative and provide a structured JSON output with:
        1. Chief Complaint: The primary reason for visit (in clinical English)
        2. History of Presenting Illness: Detailed timeline and character of symptoms
        3. Associated Symptoms: Other symptoms mentioned
        4. Duration: When symptoms started
        5. Severity: Patient's description of severity (0-10 scale)
        6. Context: What makes it better/worse
        7. Past Medical History: Any relevant history mentioned
        8. Red Flags: Any urgent/emergency indicators
        9. Confidence Score: How confident you are in the interpretation (0-1)
        10. Suggested Follow-up Questions: What else should be asked
        
        Important considerations:
        - Use the detected idioms as guidance but also look for additional expressions
        - Highlight any critical risk flags that require immediate attention
        - Maintain clinical accuracy while respecting patient's expressions
        
        Return ONLY valid JSON without any additional text.
        """
        
        return prompt
    
    def generate_soap_note(self, clinical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SOAP note from structured clinical data"""
        
        # Include risk flags in SOAP note
        risk_section = ""
        if clinical_data.get('risk_flags'):
            risk_section = "⚠️ RISK WARNINGS:\n"
            for risk in clinical_data['risk_flags']:
                risk_section += f"- {risk}\n"
        
        prompt = f"""
        Based on the following clinical data extracted from a patient interaction,
        generate a comprehensive SOAP (Subjective, Objective, Assessment, Plan) note.
        
        {risk_section}
        
        Clinical Data:
        {json.dumps(clinical_data, indent=2, ensure_ascii=False)}
        
        Generate a professional medical SOAP note with:
        
        Subjective:
        - Chief Complaint (in patient's words and clinical terms)
        - History of Presenting Illness
        - Past Medical History
        - Social History
        - Review of Systems
        
        Objective:
        - Vital signs (if available)
        - Physical exam findings (if available)
        
        Assessment:
        - Differential Diagnoses with reasoning
        - Problem List
        - Risk Assessment (include any red flags)
        
        Plan:
        - Diagnostic tests
        - Medications
        - Follow-up
        - Patient education
        - Urgency/Emergency instructions if needed
        
        Return as structured JSON.
        """
        
        try:
            if self.provider in ['openai', 'deepseek']:
                response = self._call_openai_compatible(prompt)
            elif self.provider == 'anthropic':
                response = self._call_anthropic(prompt)
            elif self.provider == 'gemini':
                response = self._call_gemini(prompt)
            
            soap_data = self._parse_soap_response(response)
            
            # Add risk flags to assessment
            if clinical_data.get('risk_flags') and 'assessment' in soap_data:
                if isinstance(soap_data['assessment'], dict):
                    soap_data['assessment']['risk_warnings'] = clinical_data['risk_flags']
                elif isinstance(soap_data['assessment'], str):
                    soap_data['assessment'] = {
                        'text': soap_data['assessment'],
                        'risk_warnings': clinical_data['risk_flags']
                    }
            
            return soap_data
            
        except Exception as e:
            logger.error(f"SOAP note generation failed: {str(e)}")
            raise
    
    def explain_transformation(self, original_text: str, clinical_output: Dict, detected_idioms: List = None) -> str:
        """Generate human-readable explanation including idiom mappings"""
        
        # Build explanation of detected idioms
        idiom_explanations = ""
        if detected_idioms:
            idiom_explanations = "Here's how we understood what you said:\n\n"
            for det in detected_idioms:
                idiom_explanations += f"• When you said '{det['idiom']}', we documented this as: {', '.join(det['clinical_terms'])}\n"
                if det.get('risk_note'):
                    idiom_explanations += f"  ⚠️ Important: {det['risk_note']}\n"
                idiom_explanations += "\n"
        
        prompt = f"""
        Patient said: "{original_text}"
        
        {idiom_explanations}
        
        Clinical summary:
        {json.dumps(clinical_output, indent=2, ensure_ascii=False)}
        
        Please provide a clear, empathetic explanation in simple English (with Urdu words where helpful)
        of how the patient's words were interpreted clinically. Include:
        1. What we understood from their description
        2. Why we documented it that way
        3. Any important warnings or next steps
        4. Validation of their experience
        
        Format the explanation in a friendly, accessible way.
        """
        
        try:
            if self.provider in ['openai', 'deepseek']:
                response = self._call_openai_compatible(prompt, temperature=0.7)
                return response.choices[0].message.content
            elif self.provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    temperature=0.7,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif self.provider == 'gemini':
                response = self.client.generate_content(prompt)
                return response.text
                
        except Exception as e:
            logger.error(f"Explanation generation failed: {str(e)}")
            return "Thank you for sharing your symptoms. Our system has analyzed them and created a clinical summary for your doctor."
    
    def _call_openai_compatible(self, prompt: str, temperature: float = 0.3):
        """Call OpenAI or compatible API (like DeepSeek)"""
        response = self.client.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are LinguaBridge Health, an AI clinical assistant specialized in South Asian healthcare communication."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=2000
        )
        return response
    
    def _call_anthropic(self, prompt: str):
        """Call Anthropic Claude API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.3,
            system="You are LinguaBridge Health, an AI clinical assistant specialized in South Asian healthcare communication.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response
    
    def _call_gemini(self, prompt: str):
        """Call Google Gemini API"""
        model = self.client.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response
    
    def _parse_clinical_response(self, response) -> Dict[str, Any]:
        """Parse AI response into structured clinical data"""
        try:
            if self.provider in ['openai', 'deepseek']:
                content = response.choices[0].message.content
            elif self.provider == 'anthropic':
                content = response.content[0].text
            elif self.provider == 'gemini':
                content = response.text
            
            # Extract JSON from response
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0].strip()
            else:
                # Try to find JSON object
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = content[start:end]
                else:
                    json_str = content.strip()
            
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {content}")
            return {
                "error": "Failed to parse AI response",
                "raw_content": content,
                "confidence_score": 0.0
            }
    
    def _parse_soap_response(self, response) -> Dict[str, Any]:
        """Parse SOAP note response"""
        return self._parse_clinical_response(response)