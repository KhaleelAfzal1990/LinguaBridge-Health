from django.core.management.base import BaseCommand
from linguabridge.apps.clinical_intake.models import Symptom, IdiomMapping

class Command(BaseCommand):
    help = 'Seed initial symptoms and idiom mappings'
    
    def handle(self, *args, **options):
        symptoms_data = [
            {
                'name': 'Chest Discomfort / Pain',
                'local_name': 'سینے میں درد / بھاری پن',
                'category': 'Cardiovascular',
                'common_idioms': ['Dil ghabra raha hai', 'Seena jal raha', 'Dil doob raha', 'Seene mein bojh', 'Gas ka dard', 'Chest heavy', 'Chest tight', 'Chest burning', 'Chest pressure'],
                'medical_terms': ['MI', 'angina', 'arrhythmia', 'hypertension', 'cardiac pain']
            },
            {
                'name': 'Palpitations',
                'local_name': 'دھڑکن تیز',
                'category': 'Cardiovascular',
                'common_idioms': ['Heart beat tez', 'Dil tez dhak dhak'],
                'medical_terms': ['arrhythmia', 'palpitations', 'tachycardia']
            },
            {
                'name': 'Shortness of Breath',
                'local_name': 'سانس پھولنا',
                'category': 'Respiratory',
                'common_idioms': ['Dum ghut raha', 'Saans phoolna', 'Hawa kam mil rahi', 'Oxygen kam', 'Breathing fast', 'Breath short', 'Suffocation', 'Shallow breathing', 'Rapid breathing'],
                'medical_terms': ['dyspnea', 'hypoxia', 'SOB', 'respiratory distress']
            },
            {
                'name': 'Cough',
                'local_name': 'کھانسی',
                'category': 'Respiratory',
                'common_idioms': ['Khansi ruk nahi rahi', 'Balgham zyada', 'Dry cough', 'Bloody cough', 'Long cough', 'Night cough', 'Chest infection', 'Fever with cough'],
                'medical_terms': ['COPD', 'pneumonia', 'bronchitis', 'tuberculosis', 'pertussis']
            },
            {
                'name': 'Wheezing',
                'local_name': 'سینے میں سیٹی / آواز',
                'category': 'Respiratory',
                'common_idioms': ['Wheezing sound', 'Seene se awaaz', 'Chest crackling', 'Lung sound', 'Night wheeze'],
                'medical_terms': ['asthma', 'COPD', 'bronchospasm', 'wheezing']
            },
            {
                'name': 'Fever',
                'local_name': 'بخار',
                'category': 'Systemic / Infectious',
                'common_idioms': ['Bukhar bar bar', 'Fever long', 'Fever unknown', 'Fever with shivering', 'Fever roz', 'Typhoid doubt', 'Dengue doubt', 'Malaria doubt', 'Viral lag gaya'],
                'medical_terms': ['sepsis', 'infection', 'pyrexia', 'PUO']
            },
            {
                'name': 'Weakness / Fatigue',
                'local_name': 'کمزوری / تھکاوٹ',
                'category': 'Systemic',
                'common_idioms': ['Thakan zyada', 'Low energy', 'Chronic fatigue', 'Weakness extreme', 'Body fatigue pain', 'Khoon ki kami'],
                'medical_terms': ['anemia', 'malignancy', 'chronic fatigue', 'cachexia', 'electrolyte imbalance']
            },
            {
                'name': 'Dizziness / Vertigo',
                'local_name': 'چکر',
                'category': 'Neurological',
                'common_idioms': ['Chakkar', 'Head spinning', 'Balance kharab', 'Dizziness', 'Behoshi', 'Fainting'],
                'medical_terms': ['vertigo', 'syncope', 'hypotension', 'labyrinthitis', 'stroke']
            },
            {
                'name': 'Headache',
                'local_name': 'سر درد',
                'category': 'Neurological',
                'common_idioms': ['Head pressure', 'Sar bhaari', 'Head heaviness', 'Headache roz', 'Migraine'],
                'medical_terms': ['migraine', 'tension headache', 'hypertension', 'sinusitis', 'stroke']
            },
            {
                'name': 'Numbness / Tingling',
                'local_name': 'سنن / جھنجھناہٹ',
                'category': 'Neurological',
                'common_idioms': ['Body numb', 'Haath sunn', 'Pair sunn', 'Tingling', 'Numbness', 'Finger numb', 'Foot numb'],
                'medical_terms': ['neuropathy', 'stroke', 'diabetes', 'nerve compression', 'paresthesia']
            },
            {
                'name': 'Abdominal Pain',
                'local_name': 'پیٹ درد',
                'category': 'Gastrointestinal',
                'common_idioms': ['Pait dard', 'Pain right side', 'Pain left side', 'Pain upper abdomen', 'Pain lower abdomen', 'Gas pressure', 'Stomach tight', 'Cramp'],
                'medical_terms': ['gastritis', 'IBS', 'GERD', 'hepatitis', 'ulcer', 'pancreatitis']
            },
            {
                'name': 'Acidity / Heartburn',
                'local_name': 'تیزابیت / سینے کی جلن',
                'category': 'Gastrointestinal',
                'common_idioms': ['Tezabiyat', 'Acidity', 'Heartburn', 'Chest burn', 'Burning gut', 'Sour taste'],
                'medical_terms': ['GERD', 'esophagitis', 'acid reflux', 'dyspepsia']
            },
            {
                'name': 'Indigestion / Bloating',
                'local_name': 'بد ہضمی / اپھارہ',
                'category': 'Gastrointestinal',
                'common_idioms': ['Appetite kam', 'Bloating', 'Food hazam nahi', 'Burping zyada', 'Fullness', 'Gas pressure'],
                'medical_terms': ['dyspepsia', 'flatulence', 'IBS', 'gastroparesis']
            },
            {
                'name': 'Nausea / Vomiting',
                'local_name': 'متلی / قے',
                'category': 'Gastrointestinal',
                'common_idioms': ['Nausea', 'Vomiting', 'Ulti', 'Vomit milk kar raha', 'Vomit smell', 'Vomit blood'],
                'medical_terms': ['gastroenteritis', 'migraine', 'food poisoning', 'hyperemesis', 'uremia']
            },
            {
                'name': 'Diarrhea',
                'local_name': 'دست',
                'category': 'Gastrointestinal',
                'common_idioms': ['Loose motion', 'Motion loose', 'Diarrhea', 'Loose stomach', 'Frequent stool', 'Stool urgency'],
                'medical_terms': ['gastroenteritis', 'IBS', 'infectious diarrhea', 'dehydration']
            },
            {
                'name': 'Constipation',
                'local_name': 'قبض',
                'category': 'Gastrointestinal',
                'common_idioms': ['Constipation', 'Stool hard', 'Pain passing stool'],
                'medical_terms': ['constipation', 'IBS-C', 'fecal impaction']
            },
            {
                'name': 'Jaundice',
                'local_name': 'یرقان',
                'category': 'Hepatic',
                'common_idioms': ['Yellow eyes', 'Yellow skin child', 'Peele ho gaye', 'Jaundice fear'],
                'medical_terms': ['hepatitis', 'liver failure', 'hyperbilirubinemia', 'neonatal jaundice']
            },
            {
                'name': 'Weight Loss (Unexplained)',
                'local_name': 'وزن کم ہونا',
                'category': 'Systemic / Metabolic',
                'common_idioms': ['Weight loss', 'Weight loss rapid', 'Appetite loss', 'Bhook nahi lagti', 'Weight kam ho gaya'],
                'medical_terms': ['malignancy', 'hyperthyroidism', 'diabetes', 'malabsorption', 'TB']
            },
            {
                'name': 'Weight Gain',
                'local_name': 'وزن بڑھنا',
                'category': 'Systemic / Metabolic',
                'common_idioms': ['Weight gain', 'Weight barh gaya', 'Body sujan', 'Fluid overload', 'Paani bhar gaya'],
                'medical_terms': ['hypothyroidism', 'PCOS', 'renal failure', 'heart failure', 'edema']
            },
            {
                'name': 'Joint Pain',
                'local_name': 'جوڑوں کا درد',
                'category': 'Musculoskeletal',
                'common_idioms': ['Joint pain', 'Ghutna dard', 'Waist pain', 'Shoulder pain', 'Arthritis pain', 'Aging joint pain'],
                'medical_terms': ['arthritis', 'osteoarthritis', 'gout', 'rheumatoid arthritis', 'ligament tear']
            },
            {
                'name': 'Back Pain',
                'local_name': 'کمر درد',
                'category': 'Musculoskeletal',
                'common_idioms': ['Back pain', 'Waist pain', 'Spine pain', 'Disc problem fear', 'Sciatica pain', 'Lower back pain'],
                'medical_terms': ['sciatica', 'spondylosis', 'PIVD', 'muscle strain', 'kidney stone']
            },
            {
                'name': 'Body Ache',
                'local_name': 'بدن درد',
                'category': 'Systemic',
                'common_idioms': ['Body pain', 'Body break', 'Body heaviness', 'Physical strain', 'Overwork pain'],
                'medical_terms': ['viral fever', 'dengue', 'myalgia', 'fibromyalgia', 'dehydration']
            },
            {
                'name': 'Swelling (Edema)',
                'local_name': 'سوجن',
                'category': 'Systemic',
                'common_idioms': ['Swelling body', 'Paani bhar gaya', 'Pairon mein sujan', 'Body sujan', 'Face swelling', 'Leg swelling', 'Soojan hai'],
                'medical_terms': ['renal failure', 'heart failure', 'hypothyroidism', 'lymphedema', 'preeclampsia']
            },
            {
                'name': 'Skin Rash / Itching',
                'local_name': 'خارش / دانے',
                'category': 'Dermatology',
                'common_idioms': ['Allergy', 'Khujli', 'Rash', 'Daad', 'Ringworm', 'Itching body', 'Skin infection', 'Red patches', 'White spots'],
                'medical_terms': ['dermatitis', 'fungal infection', 'eczema', 'psoriasis', 'scabies', 'urticaria']
            },
            {
                'name': 'Anxiety / Stress',
                'local_name': 'پریشانی / تناؤ',
                'category': 'Mental Health',
                'common_idioms': ['Tension hai', 'Stress zyada', 'Anxiety hai', 'Ghabrahat', 'Overthinking', 'Dar lagta', 'Panic attack', 'Heart racing anxiety'],
                'medical_terms': ['generalized anxiety disorder', 'panic disorder', 'PTSD', 'depression', 'somatization']
            },
            {
                'name': 'Depression / Sadness',
                'local_name': 'اداسی / ڈپریشن',
                'category': 'Mental Health',
                'common_idioms': ['Depression feel', 'Dil udaas', 'Sad without reason', 'Hopelessness', 'Crying spells', 'Emotional pain', 'Isolation feel'],
                'medical_terms': ['major depressive disorder', 'dysthymia', 'adjustment disorder']
            },
            {
                'name': 'Sleep Disturbance',
                'local_name': 'نیند نہ آنا',
                'category': 'Mental Health / Neurological',
                'common_idioms': ['Sleep problem', 'Neend nahi aati', 'Sleep disturbance', 'Neend kam', 'Night fear', 'Bad dreams'],
                'medical_terms': ['insomnia', 'sleep apnea', 'anxiety', 'depression', 'restless leg syndrome']
            },
            {
                'name': 'Memory Issues',
                'local_name': 'یادداشت کمزور',
                'category': 'Neurological / Mental Health',
                'common_idioms': ['Memory weak', 'Forgetfulness', 'Brain fog', 'Memory blackout', 'Concentration problem', 'Focus kam'],
                'medical_terms': ['dementia', 'mild cognitive impairment', 'depression', 'Alzheimer\'s', 'stroke']
            },
            {
                'name': 'Urinary Burning / Pain',
                'local_name': 'پیشاب میں جلن',
                'category': 'Urology / Nephrology',
                'common_idioms': ['Peshaab mein jalan', 'Jalan', 'Burning urine', 'Pain during urination', 'Urine burning female'],
                'medical_terms': ['UTI', 'cystitis', 'urethritis', 'STI', 'prostatitis']
            },
            {
                'name': 'Frequent Urination',
                'local_name': 'بار بار پیشاب',
                'category': 'Urology / Metabolic',
                'common_idioms': ['Urine zyada', 'Peshaab zyada', 'Frequent urination', 'Raat ko peshab', 'Night urine'],
                'medical_terms': ['diabetes', 'UTI', 'overactive bladder', 'prostate disease', 'pregnancy']
            },
            {
                'name': 'Blood in Urine',
                'local_name': 'پیشاب میں خون',
                'category': 'Urology / Nephrology',
                'common_idioms': ['Blood in urine', 'Khoon aa raha peshab'],
                'medical_terms': ['UTI', 'kidney stone', 'glomerulonephritis', 'malignancy', 'trauma']
            },
            {
                'name': 'Menstrual Problem',
                'local_name': 'ماہواری کی مشکل',
                'category': 'Obstetrics & Gynecology',
                'common_idioms': ['Periods masla', 'Periods late', 'Periods zyada', 'Periods kam', 'Irregular cycle', 'Cramps period', 'Bleeding zyada'],
                'medical_terms': ['PCOS', 'dysmenorrhea', 'menorrhagia', 'hormonal imbalance', 'menopause']
            },
            {
                'name': 'Vaginal Discharge',
                'local_name': 'سفید پانی / خارج ہونا',
                'category': 'Obstetrics & Gynecology',
                'common_idioms': ['White discharge', 'Vaginal discharge smell', 'Safed pani'],
                'medical_terms': ['vaginitis', 'STI', 'candidiasis', 'bacterial vaginosis']
            },
            {
                'name': 'Pregnancy Concern',
                'local_name': 'حمل سے متعلق',
                'category': 'Obstetrics & Gynecology',
                'common_idioms': ['Pregnancy doubt', 'Bacha thehar nahi raha', 'Morning sickness', 'Baby movement low', 'Pregnancy weakness', 'BP problem pregnancy'],
                'medical_terms': ['pregnancy', 'preeclampsia', 'hyperemesis gravidarum', 'miscarriage', 'gestational diabetes']
            },
            {
                'name': 'Infertility',
                'local_name': 'بانجھ پن',
                'category': 'Reproductive Health',
                'common_idioms': ['Infertility doubt', 'Conceive nahi ho raha', 'Fertility problem', 'Fertility tension'],
                'medical_terms': ['PCOS', 'azoospermia', 'endometriosis', 'low sperm count', 'hormonal imbalance']
            },
            {
                'name': 'Eye Strain / Vision Problem',
                'local_name': 'آنکھوں کی تکلیف',
                'category': 'Ophthalmology',
                'common_idioms': ['Nazar kamzor', 'Dhundli nazar', 'Ankhon pe parda', 'Eye pain', 'Aankh jal rahi', 'Reading problem', 'Screen se dard'],
                'medical_terms': ['cataract', 'glaucoma', 'refractive error', 'conjunctivitis', 'dry eye', 'floaters']
            },
            {
                'name': 'Hearing Problem',
                'local_name': 'سننے کی مشکل',
                'category': 'ENT',
                'common_idioms': ['Hearing kam', 'Sunai kam deta', 'Kaan band', 'Seeti awaaz', 'Ringing sound', 'Ear buzzing'],
                'medical_terms': ['hearing loss', 'tinnitus', 'otitis media', 'cerumen impaction', 'presbycusis']
            },
            {
                'name': 'Ear Pain / Discharge',
                'local_name': 'کان درد / بہنا',
                'category': 'ENT',
                'common_idioms': ['Kaan dard', 'Kaan beh raha', 'Ear discharge', 'Ear infection', 'Ear crack sound'],
                'medical_terms': ['otitis media', 'otitis externa', 'eustachian tube dysfunction', 'perforated eardrum']
            },
            {
                'name': 'Sore Throat',
                'local_name': 'گلا خراب',
                'category': 'ENT',
                'common_idioms': ['Gala kharab', 'Gala dard', 'Throat burning', 'Nigalne me dard', 'Dry throat', 'Khansi'],
                'medical_terms': ['pharyngitis', 'tonsillitis', 'laryngitis', 'strep throat']
            },
            {
                'name': 'Nasal Congestion / Runny Nose',
                'local_name': 'ناک بند / بہنا',
                'category': 'ENT',
                'common_idioms': ['Nazla', 'Naak band', 'Naak beh rahi', 'Sneezing', 'Allergy nose', 'Sinus pain', 'Blocked sinus'],
                'medical_terms': ['sinusitis', 'allergic rhinitis', 'common cold', 'nasal polyps']
            },
            {
                'name': 'Lump / Swelling (General)',
                'local_name': 'گٹھ / سوجن',
                'category': 'Oncology',
                'common_idioms': ['Ganth hai', 'Cancer shuba', 'Hard lump', 'Neck ganth', 'Breast ganth', 'Underarm ganth', 'Size barh rahi', 'Tumor doubt'],
                'medical_terms': ['malignancy', 'metastasis', 'lymphadenopathy', 'cyst', 'lipoma', 'carcinoma']
            },
            {
                'name': 'Difficulty Swallowing',
                'local_name': 'نگلنے میں دشواری',
                'category': 'Gastrointestinal / ENT',
                'common_idioms': ['Difficulty swallowing', 'Khana atak gaya', 'Food atakta', 'Nigalne me dard'],
                'medical_terms': ['dysphagia', 'esophageal stricture', 'GERD', 'throat cancer', 'globus sensation']
            },
            {
                'name': 'Bleeding (Unexplained)',
                'local_name': 'خون آنا',
                'category': 'Systemic',
                'common_idioms': ['Khoon aa raha', 'Bleeding bina wajah', 'Bloody cough', 'Stool me khoon', 'Vomit blood', 'Naak se khoon'],
                'medical_terms': ['malignancy', 'hemorrhage', 'coagulopathy', 'tuberculosis', 'ulcer', 'epistaxis']
            }
        ]

        for symptom_data in symptoms_data:
            symptom, created = Symptom.objects.get_or_create(
                name=symptom_data['name'],
                defaults={
                    'local_name': symptom_data['local_name'],
                    'category': symptom_data['category'],
                    'common_idioms': symptom_data['common_idioms'],
                    'medical_terms': symptom_data['medical_terms']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created symptom: {symptom.name}'))
            else:
                self.stdout.write(f'Symptom already exists: {symptom.name}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded symptom data'))

