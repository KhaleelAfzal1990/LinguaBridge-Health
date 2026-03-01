from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.conf import settings

class MedicalSystem(models.Model):
    """
    Represents major medical systems/body systems for clinical organization
    """
    SYSTEM_CHOICES = (
        ('cardiovascular', 'Cardiovascular System'),
        ('respiratory', 'Respiratory System'),
        ('gastrointestinal', 'Gastrointestinal System'),
        ('neurological', 'Neurological System'),
        ('musculoskeletal', 'Musculoskeletal System'),
        ('integumentary', 'Integumentary System (Skin)'),
        ('endocrine', 'Endocrine System'),
        ('genitourinary', 'Genitourinary System'),
        ('reproductive', 'Reproductive System'),
        ('psychiatric', 'Psychiatric/Mental Health'),
        ('hematologic', 'Hematologic System'),
        ('immunologic', 'Immunologic System'),
        ('renal', 'Renal/Urinary System'),
        ('hepatic', 'Hepatic/Liver System'),
        ('ophthalmic', 'Ophthalmic/Eye System'),
        ('otolaryngologic', 'Otolaryngologic/ENT System'),
        ('dental', 'Dental/Oral System'),
    )
    
    name = models.CharField(max_length=50, choices=SYSTEM_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Urdu terminology
    urdu_name = models.CharField(max_length=200, blank=True)
    common_urdu_terms = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    
    # Associated organs
    primary_organs = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    
    # Common symptoms by system
    common_symptoms = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    
    # Clinical guidelines
    assessment_guidelines = models.TextField(blank=True)
    red_flags = models.TextField(blank=True, help_text="Warning signs specific to this system")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Medical System"
        verbose_name_plural = "Medical Systems"

    def __str__(self):
        return self.display_name

    def get_urdu_display(self):
        return self.urdu_name or self.display_name


class MedicalSpecialty(models.Model):
    """
    Represents medical specialties and subspecialties
    """
    SPECIALTY_CATEGORIES = (
        ('primary', 'Primary Care'),
        ('medical', 'Medical Specialty'),
        ('surgical', 'Surgical Specialty'),
        ('diagnostic', 'Diagnostic Specialty'),
        ('supportive', 'Supportive Specialty'),
        ('subspecialty', 'Subspecialty'),
    )
    
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SPECIALTY_CATEGORIES, default='medical')
    
    # Description
    description = models.TextField(blank=True)
    scope_of_practice = models.TextField(blank=True)
    
    # Urdu terminology
    urdu_name = models.CharField(max_length=200, blank=True)
    
    # Associated medical systems
    medical_systems = models.ManyToManyField(MedicalSystem, blank=True, related_name='specialties')
    
    # Common conditions treated
    common_conditions = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    
    # Common procedures
    common_procedures = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    
    # Qualifications and training
    required_qualifications = models.TextField(blank=True)
    typical_training_years = models.IntegerField(null=True, blank=True)
    
    # Referral information
    referral_guidelines = models.TextField(blank=True)
    urgent_conditions = models.TextField(blank=True, help_text="Conditions requiring urgent referral")
    
    # Relationships
    parent_specialty = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='subspecialties')
    
    # Metadata
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Medical Specialty"
        verbose_name_plural = "Medical Specialties"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.display_name

    def get_urdu_display(self):
        return self.urdu_name or self.display_name

    def get_full_path(self):
        """Return the full specialty path (e.g., Surgery > Cardiothoracic Surgery)"""
        if self.parent_specialty:
            return f"{self.parent_specialty.get_full_path()} > {self.display_name}"
        return self.display_name


class ClinicalTerm(models.Model):
    """
    Comprehensive clinical terminology model with Urdu mappings
    """
    TERM_CATEGORIES = (
        ('symptom', 'Symptom'),
        ('sign', 'Clinical Sign'),
        ('diagnosis', 'Diagnosis'),
        ('procedure', 'Procedure'),
        ('medication', 'Medication'),
        ('anatomy', 'Anatomical Term'),
        ('lab_test', 'Laboratory Test'),
        ('vital_sign', 'Vital Sign'),
        ('risk_factor', 'Risk Factor'),
        ('complication', 'Complication'),
    )
    
    SEVERITY_LEVELS = (
        (1, 'Mild'),
        (2, 'Moderate'),
        (3, 'Severe'),
        (4, 'Life-threatening'),
    )
    
    URGENCY_LEVELS = (
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
        ('critical', 'Critical'),
    )
    
    # Basic term information
    term = models.CharField(max_length=200, unique=True, help_text="Clinical term in English")
    term_type = models.CharField(max_length=20, choices=TERM_CATEGORIES, default='symptom')
    
    # Medical system and specialty associations
    medical_system = models.ForeignKey(MedicalSystem, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='clinical_terms')
    medical_specialties = models.ManyToManyField(MedicalSpecialty, blank=True, related_name='clinical_terms')
    
    # Description and clinical context
    description = models.TextField(blank=True, help_text="Clinical description of the term")
    clinical_definition = models.TextField(blank=True, help_text="Formal medical definition")
    patient_friendly_description = models.TextField(blank=True, help_text="Simple explanation for patients")
    
    # Urdu and local language mappings
    urdu_term = models.CharField(max_length=200, blank=True, help_text="Urdu translation")
    urdu_transliteration = models.CharField(max_length=200, blank=True, help_text="Roman Urdu representation")
    regional_variations = ArrayField(models.CharField(max_length=200), blank=True, default=list,
                                    help_text="Regional variations in Urdu/Hindi")
    
    # Common idioms and expressions
    common_idioms = ArrayField(models.CharField(max_length=200), blank=True, default=list,
                              help_text="Common ways patients describe this in Urdu-English mix")
    patient_expressions = ArrayField(models.CharField(max_length=200), blank=True, default=list,
                                    help_text="Typical patient phrases")
    
    # Medical metadata
    medical_code = models.CharField(max_length=50, blank=True, help_text="ICD-10 or other medical coding")
    icd10_code = models.CharField(max_length=20, blank=True, help_text="ICD-10 code if applicable")
    snomed_ct_code = models.CharField(max_length=50, blank=True, help_text="SNOMED CT code if applicable")
    
    # Severity and urgency
    typical_severity = models.IntegerField(choices=SEVERITY_LEVELS, null=True, blank=True)
    typical_urgency = models.CharField(max_length=20, choices=URGENCY_LEVELS, default='routine')
    red_flags = models.TextField(blank=True, help_text="Warning signs that require immediate attention")
    
    # Associated symptoms and terms
    associated_symptoms = models.ManyToManyField('self', blank=True, symmetrical=False, 
                                                related_name='related_symptoms',
                                                help_text="Symptoms commonly associated with this term")
    differential_diagnoses = models.ManyToManyField('self', blank=True, symmetrical=False,
                                                   related_name='differential_for',
                                                   help_text="Conditions to consider in differential diagnosis")
    
    # Common questions for history taking
    history_questions = ArrayField(models.CharField(max_length=500), blank=True, default=list,
                                  help_text="Questions to ask when this symptom is reported")
    
    # Clinical reasoning
    clinical_pearls = models.TextField(blank=True, help_text="Important clinical insights")
    documentation_tips = models.TextField(blank=True, help_text="How to document this in medical notes")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    confidence_weight = models.FloatField(default=1.0, help_text="Weight for AI confidence scoring")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['term']
        indexes = [
            models.Index(fields=['term']),
            models.Index(fields=['term_type']),
            models.Index(fields=['medical_system']),
            models.Index(fields=['icd10_code']),
        ]
        verbose_name = "Clinical Term"
        verbose_name_plural = "Clinical Terms"

    def __str__(self):
        return f"{self.term} ({self.get_term_type_display()})"

    def get_urdu_display(self):
        """Return Urdu representation if available"""
        return self.urdu_term or self.term

    def get_patient_friendly_term(self):
        """Return patient-friendly version of the term"""
        return self.patient_friendly_description or self.description or self.term


class ClinicalSession(models.Model):
    """
    Represents a clinical intake session where patient provides symptoms
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    # Use string references
    patient = models.ForeignKey('accounts.PatientProfile', on_delete=models.CASCADE, related_name='clinical_sessions')
    doctor = models.ForeignKey('accounts.DoctorProfile', on_delete=models.CASCADE, related_name='clinical_sessions')
    
    # Medical system and specialty context
    primary_system = models.ForeignKey(MedicalSystem, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='sessions')
    primary_specialty = models.ForeignKey(MedicalSpecialty, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='sessions')
    
    session_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    audio_file = models.FileField(upload_to='audio_recordings/', null=True, blank=True)
    audio_duration = models.IntegerField(help_text='Duration in seconds', null=True, blank=True)
    raw_transcript = models.TextField(blank=True)
    processed_data = models.JSONField(default=dict)
    ai_provider_used = models.CharField(max_length=50, default='openai')
    confidence_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Add this relationship
    patient_idioms_detected = models.ManyToManyField('PatientIdiom', 
        through='SessionIdiomDetection',
        related_name='sessions',
        blank=True,
        help_text="Patient idioms detected in this session")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', '-created_at']),
            models.Index(fields=['doctor', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['primary_system']),
            models.Index(fields=['primary_specialty']),
        ]

    def __str__(self):
        return f"Session {self.id} - {self.patient} with Dr. {self.doctor} on {self.session_date}"


class Symptom(models.Model):
    """
    Symptom model linked to ClinicalTerm for backward compatibility
    """
    SEVERITY_CHOICES = (
        (1, 'Mild'),
        (2, 'Moderate'),
        (3, 'Severe'),
    )
    
    name = models.CharField(max_length=200)
    local_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    common_idioms = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    medical_terms = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    
    # Link to ClinicalTerm
    clinical_term = models.ForeignKey(ClinicalTerm, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='legacy_symptoms')
    
    # Medical system and specialty
    medical_system = models.ForeignKey(MedicalSystem, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='symptoms')
    medical_specialty = models.ForeignKey(MedicalSpecialty, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='symptoms')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['medical_system']),
        ]

    def __str__(self):
        return f"{self.name} ({self.local_name})"


class IdiomMapping(models.Model):
    """
    Maps patient idioms to clinical terms
    """
    idiom = models.CharField(max_length=500, unique=True)
    language = models.CharField(max_length=10, default='ur')  # ur, en, mix
    
    # Associations
    clinical_term = models.ForeignKey(ClinicalTerm, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='idiom_mappings')
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='idioms')
    medical_system = models.ForeignKey(MedicalSystem, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='idioms')
    medical_specialty = models.ForeignKey(MedicalSpecialty, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='idioms')
    
    confidence_weight = models.FloatField(default=1.0)
    context_notes = models.TextField(blank=True, help_text="Notes on when/how this idiom is used")
    region = models.CharField(max_length=100, blank=True, help_text="Region where this idiom is common")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['idiom']),
            models.Index(fields=['language']),
            models.Index(fields=['clinical_term']),
            models.Index(fields=['medical_system']),
        ]

    def __str__(self):
        return self.idiom

    def clean(self):
        """Ensure at least one association is set"""
        if not any([self.clinical_term, self.symptom, self.medical_system, self.medical_specialty]):
            raise ValidationError("At least one of clinical_term, symptom, medical_system, or medical_specialty must be set")


class IdiomDetectionResult(models.Model):
    """
    Stores detailed results of idiom detection from patient text
    Tracks the entire process from raw text to clinical interpretation
    """
    DETECTION_METHODS = (
        ('exact_match', 'Exact String Match'),
        ('fuzzy_match', 'Fuzzy String Match'),
        ('ai_extraction', 'AI Extraction'),
        ('contextual', 'Contextual Detection'),
        ('hybrid', 'Hybrid Method'),
    )
    
    CONFIDENCE_LEVELS = (
        ('high', 'High Confidence'),
        ('medium', 'Medium Confidence'),
        ('low', 'Low Confidence'),
        ('needs_review', 'Needs Human Review'),
    )
    
    # Core relationships
    session = models.ForeignKey(ClinicalSession, on_delete=models.CASCADE, related_name='idiom_detections')
    intake_response = models.ForeignKey('IntakeResponse', on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='idiom_detections', 
                                       help_text="The specific response where idiom was detected")
    
    # The detected idiom and its mapping
    idiom_mapping = models.ForeignKey(IdiomMapping, on_delete=models.CASCADE, related_name='detection_results',
                                     help_text="The idiom mapping that was detected")
    
    # Detection context
    original_text = models.TextField(help_text="The full original text where idiom was detected")
    matched_text = models.CharField(max_length=500, help_text="The exact text that matched the idiom")
    preceding_text = models.TextField(blank=True, help_text="Text that appears before the matched idiom")
    following_text = models.TextField(blank=True, help_text="Text that appears after the matched idiom")
    
    # Position in text
    start_index = models.IntegerField(null=True, blank=True, help_text="Start character index in original text")
    end_index = models.IntegerField(null=True, blank=True, help_text="End character index in original text")
    paragraph_index = models.IntegerField(null=True, blank=True, help_text="Paragraph number in the text")
    sentence_index = models.IntegerField(null=True, blank=True, help_text="Sentence number in the text")
    
    # Detection metadata
    detection_method = models.CharField(max_length=20, choices=DETECTION_METHODS, default='ai_extraction')
    detection_confidence = models.FloatField(default=0.0, help_text="Raw confidence score 0-1")
    confidence_level = models.CharField(max_length=20, choices=CONFIDENCE_LEVELS, default='medium')
    
    # Scoring components
    linguistic_score = models.FloatField(default=0.0, help_text="Score based on linguistic matching")
    contextual_score = models.FloatField(default=0.0, help_text="Score based on context relevance")
    semantic_score = models.FloatField(default=0.0, help_text="Score based on semantic similarity")
    temporal_score = models.FloatField(default=0.0, help_text="Score based on temporal context")
    final_score = models.FloatField(default=0.0, help_text="Weighted final score")
    
    # Clinical interpretation
    interpreted_term = models.ForeignKey(ClinicalTerm, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='detection_results',
                                        help_text="The clinical term this idiom maps to")
    alternative_interpretations = models.JSONField(default=list, blank=True,
                                                  help_text="List of alternative possible interpretations")
    interpretation_notes = models.TextField(blank=True, help_text="Notes on how this was interpreted")
    
    # Severity and urgency from context
    inferred_severity = models.IntegerField(choices=ClinicalTerm.SEVERITY_LEVELS, null=True, blank=True,
                                           help_text="Severity inferred from context")
    inferred_urgency = models.CharField(max_length=20, choices=ClinicalTerm.URGENCY_LEVELS, blank=True,
                                       help_text="Urgency inferred from context")
    
    # Temporal context
    duration_mentioned = models.CharField(max_length=100, blank=True, 
                                         help_text="Duration mentioned (e.g., '3 din se')")
    frequency_mentioned = models.CharField(max_length=100, blank=True,
                                          help_text="Frequency mentioned (e.g., 'kabhi kabhi')")
    onset_mentioned = models.CharField(max_length=100, blank=True,
                                      help_text="Onset mentioned (e.g., 'achalay')")
    
    # Validation and feedback
    is_validated = models.BooleanField(default=False, help_text="Whether this detection was validated by a professional")
    validated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='validated_idioms')
    validated_at = models.DateTimeField(null=True, blank=True)
    validation_notes = models.TextField(blank=True, help_text="Notes from validator")
    
    # User feedback
    user_rating = models.IntegerField(null=True, blank=True, help_text="User rating 1-5")
    user_feedback = models.TextField(blank=True, help_text="User feedback on detection")
    
    # For ML training
    used_in_training = models.BooleanField(default=False, help_text="Whether this was used for ML training")
    training_weight = models.FloatField(default=1.0, help_text="Weight for training data")
    
    # Metadata
    processing_time_ms = models.IntegerField(null=True, blank=True, help_text="Processing time in milliseconds")
    ai_model_version = models.CharField(max_length=50, blank=True, help_text="Version of AI model used")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session']),
            models.Index(fields=['intake_response']),
            models.Index(fields=['idiom_mapping']),
            models.Index(fields=['interpreted_term']),
            models.Index(fields=['is_validated']),
            models.Index(fields=['confidence_level']),
            models.Index(fields=['detection_method']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = "Idiom Detection Result"
        verbose_name_plural = "Idiom Detection Results"

    def __str__(self):
        return f"Idiom detection: '{self.idiom_mapping.idiom}' in session {self.session.id} (confidence: {self.confidence_level})"

    def save(self, *args, **kwargs):
        """Override save to calculate final score and confidence level"""
        if not self.final_score:
            # Calculate weighted final score
            weights = {
                'linguistic_score': 0.4,
                'contextual_score': 0.3,
                'semantic_score': 0.2,
                'temporal_score': 0.1
            }
            self.final_score = (
                self.linguistic_score * weights['linguistic_score'] +
                self.contextual_score * weights['contextual_score'] +
                self.semantic_score * weights['semantic_score'] +
                self.temporal_score * weights['temporal_score']
            )
        
        # Set confidence level based on final score
        if self.final_score >= 0.8:
            self.confidence_level = 'high'
        elif self.final_score >= 0.6:
            self.confidence_level = 'medium'
        elif self.final_score >= 0.4:
            self.confidence_level = 'low'
        else:
            self.confidence_level = 'needs_review'
        
        super().save(*args, **kwargs)

    def get_context_window(self, window_size=50):
        """Get context window around the detected idiom"""
        start = max(0, self.start_index - window_size) if self.start_index else 0
        end = min(len(self.original_text), self.end_index + window_size) if self.end_index else len(self.original_text)
        return self.original_text[start:end]

    def get_surrounding_sentences(self):
        """Extract the sentence containing the idiom and surrounding sentences"""
        sentences = self.original_text.split('. ')
        for i, sentence in enumerate(sentences):
            if self.matched_text in sentence:
                context = {
                    'previous': sentences[i-1] if i > 0 else '',
                    'current': sentence,
                    'next': sentences[i+1] if i < len(sentences) - 1 else ''
                }
                return context
        return None


class IntakeResponse(models.Model):
    """
    Individual responses during the intake process
    """
    session = models.ForeignKey(ClinicalSession, on_delete=models.CASCADE, related_name='responses')
    question = models.TextField()
    response_text = models.TextField()
    response_audio = models.FileField(upload_to='response_audio/', null=True, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    urgency_score = models.FloatField(null=True, blank=True)
    
    # AI analysis
    identified_terms = models.ManyToManyField(ClinicalTerm, blank=True, through='ResponseTermAnalysis')
    
    # System and specialty classification
    primary_system = models.ForeignKey(MedicalSystem, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='responses')
    primary_specialty = models.ForeignKey(MedicalSpecialty, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='responses')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Response {self.id} for session {self.session.id}"


class ResponseTermAnalysis(models.Model):
    """
    Analysis of terms identified in a specific response
    """
    response = models.ForeignKey(IntakeResponse, on_delete=models.CASCADE, related_name='term_analyses')
    clinical_term = models.ForeignKey(ClinicalTerm, on_delete=models.CASCADE, related_name='response_analyses')
    
    confidence = models.FloatField(default=0.0)
    context = models.TextField(blank=True)
    exact_phrase = models.CharField(max_length=500, blank=True, help_text="The exact phrase that matched")
    matched_idiom = models.ForeignKey(IdiomMapping, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='term_analyses')
    
    # System classification confidence
    system_confidence = models.FloatField(default=0.0)
    specialty_confidence = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['response']),
            models.Index(fields=['clinical_term']),
        ]

    def __str__(self):
        return f"Analysis: {self.clinical_term.term} in response {self.response.id}"


class ClinicalSummary(models.Model):
    """
    Structured clinical summary of the session
    """
    SUMMARY_TYPES = (
        ('chief_complaint', 'Chief Complaint'),
        ('history', 'Clinical History'),
        ('soap_note', 'SOAP Note'),
        ('referral', 'Referral Summary'),
    )
    
    session = models.OneToOneField(ClinicalSession, on_delete=models.CASCADE, related_name='summary')
    summary_type = models.CharField(max_length=20, choices=SUMMARY_TYPES, default='soap_note')
    content = models.JSONField()
    explanation = models.TextField(blank=True)
    doctor_approved = models.BooleanField(default=False)
    doctor_notes = models.TextField(blank=True)
    
    # For SOAP notes
    subjective = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    plan = models.TextField(blank=True)
    
    # Referral information
    referral_specialty = models.ForeignKey(MedicalSpecialty, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='referral_summaries')
    referral_urgency = models.CharField(max_length=20, choices=ClinicalTerm.URGENCY_LEVELS, default='routine')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['session', 'summary_type']),
        ]

    def __str__(self):
        return f"Summary for session {self.session.id} - {self.get_summary_type_display()}"


class PatientIdiom(models.Model):
    """
    Tracks idiom usage patterns for individual patients over time
    Learns how specific patients express symptoms and builds a personal language profile
    """
    CONFIDENCE_LEVELS = (
        ('established', 'Established Pattern'),
        ('emerging', 'Emerging Pattern'),
        ('possible', 'Possible Match'),
        ('one_off', 'One-time Usage'),
    )
    
    # Core relationships
    patient = models.ForeignKey('accounts.PatientProfile', on_delete=models.CASCADE, 
                                related_name='patient_idioms')
    idiom_mapping = models.ForeignKey(IdiomMapping, on_delete=models.CASCADE,
                                     related_name='patient_usages',
                                     help_text="The idiom mapping this patient uses")
    
    # Usage statistics
    first_used = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    usage_count = models.IntegerField(default=1, help_text="Number of times this patient has used this idiom")
    
    # Confidence for this specific patient
    patient_confidence = models.FloatField(default=0.5, 
        help_text="Confidence score specific to this patient (0-1)")
    confidence_level = models.CharField(max_length=20, choices=CONFIDENCE_LEVELS, default='possible')
    
    # Context patterns
    typical_contexts = models.JSONField(default=list, blank=True,
        help_text="Common contexts where this patient uses this idiom")
    typical_severity = models.IntegerField(choices=ClinicalTerm.SEVERITY_LEVELS, null=True, blank=True,
        help_text="Typical severity level for this patient when using this idiom")
    typical_urgency = models.CharField(max_length=20, choices=ClinicalTerm.URGENCY_LEVELS, blank=True,
        help_text="Typical urgency level for this patient")
    
    # Associated symptoms (for this patient specifically)
    associated_symptoms = models.ManyToManyField('self', blank=True, symmetrical=False,
        help_text="Symptoms this patient often mentions together")
    
    # Temporal patterns
    common_times = models.JSONField(default=list, blank=True,
        help_text="Times of day when this idiom is commonly used")
    seasonal_patterns = models.JSONField(default=list, blank=True,
        help_text="Seasonal patterns (e.g., 'winter', 'monsoon')")
    
    # Linguistic variations (how this patient specifically phrases it)
    personal_variations = ArrayField(models.CharField(max_length=500), blank=True, default=list,
        help_text="Personal variations of the idiom this patient uses")
    preferred_terms = ArrayField(models.CharField(max_length=200), blank=True, default=list,
        help_text="Clinical terms this patient prefers or responds to")
    
    # Clinical associations for this patient
    associated_conditions = models.ManyToManyField(ClinicalTerm, blank=True,
        related_name='patient_idiom_conditions',
        help_text="Medical conditions this idiom typically indicates for this patient")
    
    # Recent clinical sessions where this idiom was detected
    recent_sessions = models.ManyToManyField(ClinicalSession, blank=True,
        help_text="Recent sessions where this idiom was used")
    
    # Last detection details
    last_detection = models.ForeignKey(IdiomDetectionResult, on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='+')
    last_detection_text = models.TextField(blank=True, help_text="The exact text from last detection")
    
    # Accuracy and validation
    accuracy_score = models.FloatField(default=0.0, help_text="How often this interpretation was correct")
    times_validated = models.IntegerField(default=0, help_text="Number of times validated by doctor")
    times_correct = models.IntegerField(default=0, help_text="Number of times interpretation was correct")
    doctor_feedback = models.JSONField(default=list, blank=True,
        help_text="Feedback from doctors about this patient's idiom usage")
    
    # Learning parameters
    learning_rate = models.FloatField(default=0.1, help_text="How quickly to adapt to new patterns")
    weight_factor = models.FloatField(default=1.0, help_text="Weight in personalization algorithms")
    is_active = models.BooleanField(default=True, help_text="Whether to continue tracking this idiom")
    
    # Metadata
    notes = models.TextField(blank=True, help_text="Clinical notes about this patient's language patterns")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-usage_count', '-last_used']
        unique_together = ['patient', 'idiom_mapping']  # One record per patient-idiom pair
        indexes = [
            models.Index(fields=['patient', '-usage_count']),
            models.Index(fields=['patient', '-last_used']),
            models.Index(fields=['patient', 'confidence_level']),
            models.Index(fields=['idiom_mapping']),
            models.Index(fields=['patient_confidence']),
        ]
        verbose_name = "Patient Idiom"
        verbose_name_plural = "Patient Idioms"

    def __str__(self):
        return f"{self.patient} - {self.idiom_mapping.idiom} (used {self.usage_count}x)"

    def save(self, *args, **kwargs):
        """Update confidence level based on usage and accuracy"""
        if not self.pk:  # New record
            self.confidence_level = 'possible'
        
        # Update confidence level based on usage count and accuracy
        if self.usage_count >= 5 and self.accuracy_score >= 0.8:
            self.confidence_level = 'established'
        elif self.usage_count >= 3 and self.accuracy_score >= 0.6:
            self.confidence_level = 'emerging'
        elif self.usage_count == 1:
            self.confidence_level = 'one_off'
        
        # Calculate patient-specific confidence
        base_confidence = self.idiom_mapping.confidence_weight if self.idiom_mapping else 0.5
        usage_factor = min(self.usage_count / 10, 1.0)  # Max out at 10 uses
        accuracy_factor = self.accuracy_score
        
        self.patient_confidence = (base_confidence * 0.3 + 
                                   usage_factor * 0.3 + 
                                   accuracy_factor * 0.4)
        
        super().save(*args, **kwargs)

    def record_usage(self, detection_result, session, context=None):
        """
        Record a new usage of this idiom by the patient
        """
        from django.utils import timezone
        
        self.usage_count += 1
        self.last_used = timezone.now()
        self.last_detection = detection_result
        self.last_detection_text = detection_result.matched_text if detection_result else ""
        
        # Update recent sessions
        self.recent_sessions.add(session)
        
        # Keep only last 10 sessions
        if self.recent_sessions.count() > 10:
            oldest = self.recent_sessions.order_by('-session_date').last()
            if oldest:
                self.recent_sessions.remove(oldest)
        
        # Update typical contexts
        if context:
            contexts = self.typical_contexts or []
            contexts.append({
                'context': context,
                'timestamp': timezone.now().isoformat(),
                'session_id': session.id
            })
            # Keep last 20 contexts
            self.typical_contexts = contexts[-20:]
        
        # Update temporal patterns
        current_hour = timezone.now().hour
        hour_pattern = f"{current_hour:02d}:00"
        times = self.common_times or []
        times.append(hour_pattern)
        # Keep last 50 time stamps
        self.common_times = times[-50:]
        
        self.save()

    def record_validation(self, was_correct, doctor=None, feedback=None):
        """
        Record doctor validation feedback
        """
        self.times_validated += 1
        if was_correct:
            self.times_correct += 1
        
        # Update accuracy score
        self.accuracy_score = self.times_correct / self.times_validated if self.times_validated > 0 else 0
        
        # Store feedback if provided
        if feedback and doctor:
            from django.utils import timezone
            feedback_entry = {
                'doctor': str(doctor),
                'feedback': feedback,
                'was_correct': was_correct,
                'timestamp': timezone.now().isoformat()
            }
            feedback_list = self.doctor_feedback or []
            feedback_list.append(feedback_entry)
            self.doctor_feedback = feedback_list[-20:]  # Keep last 20 feedback entries
        
        self.save()

    def get_personalized_interpretation(self):
        """
        Get a personalized interpretation based on this patient's history
        """
        interpretation = {
            'idiom': self.idiom_mapping.idiom,
            'clinical_term': str(self.idiom_mapping.clinical_term) if self.idiom_mapping.clinical_term else None,
            'patient_confidence': self.patient_confidence,
            'confidence_level': self.confidence_level,
            'typical_severity': self.get_typical_severity_display() if self.typical_severity else None,
            'typical_urgency': self.get_typical_urgency_display() if self.typical_urgency else None,
            'usage_count': self.usage_count,
            'accuracy': self.accuracy_score,
            'notes': self.notes if self.notes else None
        }
        return interpretation

    def get_common_associations(self):
        """
        Get symptoms commonly associated with this idiom for this patient
        """
        associations = []
        for idiom in self.associated_symptoms.all():
            associations.append({
                'idiom': idiom.idiom_mapping.idiom,
                'clinical_term': str(idiom.idiom_mapping.clinical_term) if idiom.idiom_mapping.clinical_term else None,
                'frequency': idiom.usage_count
            })
        return sorted(associations, key=lambda x: x['frequency'], reverse=True)


class DoctorProfile(models.Model):
    """Doctor profile model"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clinical_intakedoctor_profile')
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=100)
    qualifications = models.TextField()
    experience_years = models.IntegerField()
    clinic_name = models.CharField(max_length=200)
    clinic_address = models.TextField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_days = models.JSONField(default=list)  # ['Monday', 'Wednesday']
    available_time_start = models.TimeField(null=True, blank=True)
    available_time_end = models.TimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"


class PatientProfile(models.Model):
    """Patient profile model"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clinical_intakepatient_profile')
    
    # Basic medical information
    blood_group = models.CharField(max_length=5, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    
    # Medical history
    allergies = models.TextField(blank=True, help_text="List of allergies")
    chronic_conditions = models.TextField(blank=True, help_text="Existing chronic conditions")
    current_medications = models.TextField(blank=True, help_text="Current medications")
    past_surgeries = models.TextField(blank=True, help_text="History of surgeries")
    family_history = models.TextField(blank=True, help_text="Family medical history")
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    
    # Healthcare preferences
    preferred_doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, 
                                        related_name='preferred_patients')
    preferred_language = models.CharField(max_length=10, default='ur', 
                                         help_text="Preferred language for communication")
    preferred_clinic = models.ForeignKey('Clinic', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='preferred_patients')
    
    # Insurance information
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_id = models.CharField(max_length=50, blank=True)
    
    # Consent and privacy
    consent_given = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    data_sharing_consent = models.BooleanField(default=False)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['blood_group']),
            models.Index(fields=['preferred_doctor']),
        ]
    
    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"

    def calculate_age(self):
        """Calculate patient's age from date of birth"""
        if self.user.date_of_birth:
            from django.utils import timezone
            today = timezone.now().date()
            return today.year - self.user.date_of_birth.year - (
                (today.month, today.day) < (self.user.date_of_birth.month, self.user.date_of_birth.day)
            )
        return None

    def get_bmi(self):
        """Calculate BMI if height and weight are available"""
        if self.height and self.weight and self.height > 0:
            height_m = self.height / 100  # Convert cm to m
            bmi = self.weight / (height_m * height_m)
            return round(bmi, 1)
        return None


class Clinic(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Pakistan')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    registration_number = models.CharField(max_length=50, unique=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='managed_clinics')
    doctors = models.ManyToManyField(DoctorProfile, related_name='clinics', blank=True)
    
    # Clinic details
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class PatientMedicalHistory(models.Model):
    """Detailed medical history for patients"""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_history')
    
    HISTORY_TYPES = (
        ('condition', 'Medical Condition'),
        ('surgery', 'Surgery'),
        ('medication', 'Medication'),
        ('allergy', 'Allergy'),
        ('immunization', 'Immunization'),
        ('test', 'Medical Test'),
    )
    
    history_type = models.CharField(max_length=20, choices=HISTORY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_diagnosed = models.DateField(null=True, blank=True)
    date_resolved = models.DateField(null=True, blank=True)
    is_chronic = models.BooleanField(default=False)
    
    # Doctor who diagnosed/treated
    diagnosed_by = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Attachments (reports, prescriptions)
    attachments = models.JSONField(default=list, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_diagnosed', '-created_at']
        indexes = [
            models.Index(fields=['patient', 'history_type']),
            models.Index(fields=['patient', 'date_diagnosed']),
        ]
    
    def __str__(self):
        return f"{self.get_history_type_display()}: {self.title} for {self.patient}"


class PatientLanguageProfile(models.Model):
    """
    Overall language profile for a patient
    Aggregates all patient idioms and provides a complete picture
    """
    patient = models.OneToOneField('accounts.PatientProfile', on_delete=models.CASCADE,
                                   related_name='language_profile')
    
    # Demographics for language patterns
    age_group = models.CharField(max_length=20, blank=True, help_text="e.g., child, adult, elderly")
    education_level = models.CharField(max_length=50, blank=True)
    primary_language = models.CharField(max_length=50, default='Urdu')
    secondary_languages = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    region = models.CharField(max_length=100, blank=True, help_text="Geographic region")
    
    # Language preferences
    preferred_terminology = models.CharField(max_length=20, choices=(
        ('simple', 'Simple Terms'),
        ('mixed', 'Mixed Urdu-English'),
        ('clinical', 'Clinical Terms'),
        ('urdu', 'Urdu Only'),
    ), default='mixed')
    
    preferred_explanations = models.CharField(max_length=20, choices=(
        ('simple', 'Simple Explanations'),
        ('detailed', 'Detailed Explanations'),
        ('visual', 'Visual Explanations'),
    ), default='simple')
    
    # Communication style
    communication_style = models.JSONField(default=dict, blank=True,
        help_text="Communication preferences and patterns")
    
    # Summary statistics
    total_idioms_used = models.IntegerField(default=0)
    unique_idioms_count = models.IntegerField(default=0)
    most_used_idioms = models.JSONField(default=list, blank=True)
    
    # Learning model data (serialized for ML)
    embedding_vector = models.JSONField(null=True, blank=True,
        help_text="Vector representation of patient's language patterns")
    language_model_state = models.JSONField(null=True, blank=True,
        help_text="Serialized state of personalized language model")
    
    # Last analysis
    last_analyzed = models.DateTimeField(null=True, blank=True)
    analysis_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Patient Language Profile"
        verbose_name_plural = "Patient Language Profiles"

    def __str__(self):
        return f"Language Profile for {self.patient}"

    def update_from_idioms(self):
        """Update profile statistics from patient idioms"""
        idioms = PatientIdiom.objects.filter(patient=self.patient, is_active=True)
        
        self.total_idioms_used = idioms.aggregate(models.Sum('usage_count'))['usage_count__sum'] or 0
        self.unique_idioms_count = idioms.count()
        
        # Get most used idioms
        top_idioms = idioms.order_by('-usage_count')[:10]
        self.most_used_idioms = [
            {
                'idiom': idiom.idiom_mapping.idiom,
                'count': idiom.usage_count,
                'confidence': idiom.patient_confidence
            }
            for idiom in top_idioms
        ]
        
        from django.utils import timezone
        self.last_analyzed = timezone.now()
        self.save()


class SessionIdiomDetection(models.Model):
    """
    Tracks which patient idioms were detected in which sessions
    """
    session = models.ForeignKey(ClinicalSession, on_delete=models.CASCADE)
    patient_idiom = models.ForeignKey(PatientIdiom, on_delete=models.CASCADE)
    detection_result = models.ForeignKey(IdiomDetectionResult, on_delete=models.CASCADE)
    
    # Detection context
    confidence_at_time = models.FloatField(default=0.0)
    was_validated = models.BooleanField(default=False)
    doctor_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['session', 'patient_idiom', 'detection_result']


# Signal to create initial Medical Systems and Specialties
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_initial_clinical_data(sender, **kwargs):
    """Create initial clinical terminology data after migrations"""
    if sender.name == 'apps.clinical_intake':
        
        # Create Medical Systems
        medical_systems = [
            # (name, display_name, urdu_name, common_urdu_terms)
            ('cardiovascular', 'Cardiovascular System', 'دورانِ خون کا نظام', 
             ['dil', 'qalb', 'khoon ki naliyan', 'shariyan']),
            ('respiratory', 'Respiratory System', 'نظامِ تنفس', 
             ['saans', 'phephray', 'sina', 'dam']),
            ('gastrointestinal', 'Gastrointestinal System', 'نظامِ ہضم', 
             ['paet', 'antriyan', 'hazma', 'meda']),
            ('neurological', 'Neurological System', 'نظامِ اعصاب', 
             ['dimagh', 'aasab', 'reerh ki haddi', 'nos']),
            ('musculoskeletal', 'Musculoskeletal System', 'نظامِ حرکت', 
             ['haddiyan', 'patey', 'jor', 'azlaat']),
            ('endocrine', 'Endocrine System', 'نظامِ غدود', 
             ['ghudud', 'harmones', 'thyroid']),
            ('renal', 'Renal/Urinary System', 'نظامِ ادرار', 
             ['gurday', 'peshab', 'pathri']),
        ]
        
        created_systems = {}
        for name, display_name, urdu_name, urdu_terms in medical_systems:
            system, created = MedicalSystem.objects.get_or_create(
                name=name,
                defaults={
                    'display_name': display_name,
                    'urdu_name': urdu_name,
                    'common_urdu_terms': urdu_terms,
                    'description': f"Medical system covering {display_name.lower()}",
                }
            )
            created_systems[name] = system
        
        # Create Medical Specialties
        medical_specialties = [
            # (name, display_name, category, urdu_name, systems)
            ('cardiology', 'Cardiology', 'medical', 'امراضِ قلب', ['cardiovascular']),
            ('pulmonology', 'Pulmonology', 'medical', 'امراضِ صدر', ['respiratory']),
            ('gastroenterology', 'Gastroenterology', 'medical', 'امراضِ معدہ و امعاء', ['gastrointestinal']),
            ('neurology', 'Neurology', 'medical', 'امراضِ اعصاب', ['neurological']),
            ('orthopedics', 'Orthopedics', 'surgical', 'امراضِ استخوان', ['musculoskeletal']),
            ('endocrinology', 'Endocrinology', 'medical', 'امراضِ غدود', ['endocrine']),
            ('nephrology', 'Nephrology', 'medical', 'امراضِ گردہ', ['renal']),
            ('general_medicine', 'General Medicine', 'primary', 'معالجہ', 
             ['cardiovascular', 'respiratory', 'gastrointestinal', 'neurological', 'endocrine']),
            ('family_medicine', 'Family Medicine', 'primary', 'خاندانی معالجہ', 
             ['cardiovascular', 'respiratory', 'gastrointestinal', 'endocrine', 'musculoskeletal']),
        ]
        
        for name, display_name, category, urdu_name, system_names in medical_specialties:
            specialty, created = MedicalSpecialty.objects.get_or_create(
                name=name,
                defaults={
                    'display_name': display_name,
                    'category': category,
                    'urdu_name': urdu_name,
                    'description': f"{display_name} specialty",
                }
            )
            
            # Add medical systems
            for system_name in system_names:
                if system_name in created_systems:
                    specialty.medical_systems.add(created_systems[system_name])
        
        # Create initial Clinical Terms
        initial_terms = [
            {
                'term': 'Dyspnea',
                'term_type': 'symptom',
                'medical_system': created_systems.get('respiratory'),
                'description': 'Difficult or labored breathing',
                'patient_friendly_description': 'Shortness of breath or difficulty breathing',
                'urdu_term': 'سانس پھولنا',
                'urdu_transliteration': 'Saans phoolna',
                'common_idioms': ['saans phoolna', 'saans nahi aana', 'dam phoolna'],
                'icd10_code': 'R06.0',
                'typical_urgency': 'urgent',
                'red_flags': 'Sudden onset, chest pain, cyanosis'
            },
            {
                'term': 'Chest Pain',
                'term_type': 'symptom',
                'medical_system': created_systems.get('cardiovascular'),
                'description': 'Pain or discomfort in the chest area',
                'patient_friendly_description': 'Pain or pressure in the chest',
                'urdu_term': 'سینے میں درد',
                'urdu_transliteration': 'Seene mein dard',
                'common_idioms': ['seene mein dard', 'chest heavy', 'dil mein dard'],
                'icd10_code': 'R07.9',
                'typical_urgency': 'emergency',
                'red_flags': 'Radiating to arm/jaw, with sweating, nausea'
            },
            {
                'term': 'Palpitations',
                'term_type': 'symptom',
                'medical_system': created_systems.get('cardiovascular'),
                'description': 'Awareness of heartbeat, feeling of rapid or irregular heartbeat',
                'patient_friendly_description': 'Feeling your heart pounding or racing',
                'urdu_term': 'دل کی دھڑکن',
                'urdu_transliteration': 'Dil ki dharkan',
                'common_idioms': ['dil dhak dhak', 'dil tez dharakna'],
                'icd10_code': 'R00.2',
                'typical_urgency': 'urgent'
            },
        ]
        
        for term_data in initial_terms:
            term, created = ClinicalTerm.objects.get_or_create(
                term=term_data['term'],
                defaults=term_data
            )
            
            # Create IdiomMappings for common idioms
            if created and 'common_idioms' in term_data:
                for idiom_text in term_data['common_idioms']:
                    IdiomMapping.objects.get_or_create(
                        idiom=idiom_text,
                        defaults={
                            'language': 'ur',
                            'clinical_term': term,
                            'confidence_weight': 0.9
                        }
                    )