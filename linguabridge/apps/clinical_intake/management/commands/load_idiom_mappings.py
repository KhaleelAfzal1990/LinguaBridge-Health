import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.clinical_intake.models import (
    PatientIdiom, MedicalSystem, MedicalSpecialty, ClinicalTerm
)

class Command(BaseCommand):
    help = 'Load idiom mappings from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing idiom mappings')

    @transaction.atomic
    def handle(self, *args, **options):
        json_file = options['json_file']
        
        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f'File {json_file} does not exist'))
            return

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Track statistics
        stats = {
            'idioms_processed': 0,
            'systems_created': 0,
            'specialties_created': 0,
            'terms_created': 0,
            'errors': 0
        }

        # Cache for systems and specialties to avoid duplicates
        systems_cache = {}
        specialties_cache = {}
        terms_cache = {}

        for idiom_text, mapping in data.items():
            try:
                self.stdout.write(f"Processing: {idiom_text}")
                
                # Get or create medical system
                system_name = mapping.get('system', 'Unknown')
                if system_name not in systems_cache:
                    system, created = MedicalSystem.objects.get_or_create(
                        name=system_name
                    )
                    systems_cache[system_name] = system
                    if created:
                        stats['systems_created'] += 1
                        self.stdout.write(f"  Created system: {system_name}")
                else:
                    system = systems_cache[system_name]

                # Get or create medical specialty
                specialty_name = mapping.get('specialty', 'Unknown')
                cache_key = f"{system_name}:{specialty_name}"
                if cache_key not in specialties_cache:
                    specialty, created = MedicalSpecialty.objects.get_or_create(
                        name=specialty_name,
                        system=system
                    )
                    specialties_cache[cache_key] = specialty
                    if created:
                        stats['specialties_created'] += 1
                        self.stdout.write(f"  Created specialty: {specialty_name}")
                else:
                    specialty = specialties_cache[cache_key]

                # Process clinical terms
                clinical_terms_text = mapping.get('clinical', '')
                clinical_term_list = [term.strip() for term in clinical_terms_text.split(';') if term.strip()]
                
                # Get or create the idiom
                idiom, created = PatientIdiom.objects.get_or_create(
                    idiom=idiom_text,
                    defaults={
                        'primary_system': system,
                        'primary_specialty': specialty,
                        'risk_note': mapping.get('risk_note', ''),
                        'confidence_weight': 1.0
                    }
                )

                if created:
                    stats['idioms_processed'] += 1
                    self.stdout.write(f"  Created idiom: {idiom_text}")
                else:
                    # Update existing idiom
                    idiom.primary_system = system
                    idiom.primary_specialty = specialty
                    idiom.risk_note = mapping.get('risk_note', '')
                    idiom.save()
                    self.stdout.write(f"  Updated idiom: {idiom_text}")

                # Process and link clinical terms
                for term_text in clinical_term_list:
                    if term_text not in terms_cache:
                        term, created = ClinicalTerm.objects.get_or_create(
                            term=term_text,
                            defaults={
                                'system': system,
                                'specialty': specialty,
                                'full_form': self._get_term_full_form(term_text)
                            }
                        )
                        terms_cache[term_text] = term
                        if created:
                            stats['terms_created'] += 1
                            self.stdout.write(f"    Created term: {term_text}")
                    else:
                        term = terms_cache[term_text]

                    # Link term to idiom if not already linked
                    idiom.clinical_terms.add(term)

                self.stdout.write(self.style.SUCCESS(f"  Successfully processed: {idiom_text}"))

            except Exception as e:
                stats['errors'] += 1
                self.stdout.write(self.style.ERROR(f"Error processing {idiom_text}: {str(e)}"))

        # Print summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('IMPORT COMPLETE'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f"Idioms processed: {stats['idioms_processed']}")
        self.stdout.write(f"Medical systems created: {stats['systems_created']}")
        self.stdout.write(f"Medical specialties created: {stats['specialties_created']}")
        self.stdout.write(f"Clinical terms created: {stats['terms_created']}")
        self.stdout.write(f"Errors: {stats['errors']}")
        
        if stats['errors'] == 0:
            self.stdout.write(self.style.SUCCESS('All idioms loaded successfully!'))
        else:
            self.stdout.write(self.style.WARNING(f'Completed with {stats["errors"]} errors'))

    def _get_term_full_form(self, term):
        """Get full form for common medical abbreviations"""
        full_forms = {
            'MI': 'Myocardial Infarction',
            'angina': 'Angina Pectoris',
            'arrhythmia': 'Cardiac Arrhythmia',
            'hypertension': 'Hypertension',
            'COPD': 'Chronic Obstructive Pulmonary Disease',
            'DM': 'Diabetes Mellitus',
            'CKD': 'Chronic Kidney Disease',
            'UTI': 'Urinary Tract Infection',
            'GERD': 'Gastroesophageal Reflux Disease',
            'IBS': 'Irritable Bowel Syndrome',
        }
        return full_forms.get(term, '')