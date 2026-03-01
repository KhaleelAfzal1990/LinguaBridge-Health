LinguaBridge Health
We turn how patients speak into how doctors think.

LinguaBridge Health is an AI-powered clinical intake engine designed for Urdu–English code-mixed healthcare environments.

openapi: 3.0.3
info:
  title: ''
  version: 0.0.0
paths:
  /api/auth/clinics/:
    get:
      operationId: auth_clinics_list
      parameters:
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      tags:
      - auth
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedClinicList'
          description: ''
    post:
      operationId: auth_clinics_create
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Clinic'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Clinic'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Clinic'
        required: true
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Clinic'
          description: ''
  /api/auth/clinics/{id}/:
    get:
      operationId: auth_clinics_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - auth
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Clinic'
          description: ''
    put:
      operationId: auth_clinics_update
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Clinic'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Clinic'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Clinic'
        required: true
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Clinic'
          description: ''
    patch:
      operationId: auth_clinics_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedClinic'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedClinic'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedClinic'
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Clinic'
          description: ''
    delete:
      operationId: auth_clinics_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - auth
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/auth/doctor/profile/:
    get:
      operationId: auth_doctor_profile_retrieve
      tags:
      - auth
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DoctorProfile'
          description: ''
    put:
      operationId: auth_doctor_profile_update
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DoctorProfile'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/DoctorProfile'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/DoctorProfile'
        required: true
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DoctorProfile'
          description: ''
    patch:
      operationId: auth_doctor_profile_partial_update
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedDoctorProfile'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedDoctorProfile'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedDoctorProfile'
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DoctorProfile'
          description: ''
  /api/auth/login/:
    post:
      operationId: auth_login_create
      tags:
      - auth
      security:
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          description: No response body
  /api/auth/logout/:
    post:
      operationId: auth_logout_create
      tags:
      - auth
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/auth/me/:
    get:
      operationId: auth_me_retrieve
      tags:
      - auth
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
          description: ''
    put:
      operationId: auth_me_update
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/User'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/User'
        required: true
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
          description: ''
    patch:
      operationId: auth_me_partial_update
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedUser'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedUser'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedUser'
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
          description: ''
  /api/auth/patient/profile/:
    get:
      operationId: auth_patient_profile_retrieve
      tags:
      - auth
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PatientProfile'
          description: ''
    put:
      operationId: auth_patient_profile_update
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatientProfile'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatientProfile'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatientProfile'
        required: true
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PatientProfile'
          description: ''
    patch:
      operationId: auth_patient_profile_partial_update
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedPatientProfile'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedPatientProfile'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedPatientProfile'
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PatientProfile'
          description: ''
  /api/auth/register/:
    post:
      operationId: auth_register_create
      tags:
      - auth
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Register'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Register'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Register'
        required: true
      security:
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Register'
          description: ''
  /api/consultations/appointments/:
    get:
      operationId: consultations_appointments_list
      parameters:
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      tags:
      - consultations
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAppointmentList'
          description: ''
    post:
      operationId: consultations_appointments_create
      tags:
      - consultations
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Appointment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Appointment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Appointment'
        required: true
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Appointment'
          description: ''
  /api/consultations/appointments/{appointment_id}/start/:
    post:
      operationId: consultations_appointments_start_create
      description: Start a consultation based on appointment and clinical session
      parameters:
      - in: path
        name: appointment_id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/consultations/appointments/{id}/:
    get:
      operationId: consultations_appointments_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Appointment'
          description: ''
    put:
      operationId: consultations_appointments_update
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Appointment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Appointment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Appointment'
        required: true
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Appointment'
          description: ''
    patch:
      operationId: consultations_appointments_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedAppointment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedAppointment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedAppointment'
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Appointment'
          description: ''
    delete:
      operationId: consultations_appointments_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/consultations/consultations/{consultation_id}/complete/:
    post:
      operationId: consultations_consultations_complete_create
      description: Complete the consultation and generate final documents
      parameters:
      - in: path
        name: consultation_id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/consultations/consultations/{consultation_id}/prescriptions/:
    post:
      operationId: consultations_consultations_prescriptions_create
      description: Add prescription to consultation
      parameters:
      - in: path
        name: consultation_id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/consultations/consultations/{consultation_id}/referrals/:
    post:
      operationId: consultations_consultations_referrals_create
      description: Generate referral summary using AI
      parameters:
      - in: path
        name: consultation_id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/consultations/consultations/{id}/:
    get:
      operationId: consultations_consultations_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Consultation'
          description: ''
    put:
      operationId: consultations_consultations_update
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Consultation'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Consultation'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Consultation'
        required: true
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Consultation'
          description: ''
    patch:
      operationId: consultations_consultations_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - consultations
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedConsultation'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedConsultation'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedConsultation'
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Consultation'
          description: ''
  /api/intake/detect-idioms/:
    post:
      operationId: intake_detect_idioms_create
      description: |-
        Only detect idioms without full AI processing
        Useful for quick checks or pre-processing
      tags:
      - intake
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/intake/idioms/:
    get:
      operationId: intake_idioms_list
      description: List all patient idioms with their clinical mappings
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      tags:
      - intake
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedPatientIdiomList'
          description: ''
  /api/intake/process/:
    post:
      operationId: intake_process_create
      description: Process patient narrative (text or audio) and return structured
        clinical data
      tags:
      - intake
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/intake/sessions/:
    get:
      operationId: intake_sessions_list
      parameters:
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      tags:
      - intake
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedClinicalSessionList'
          description: ''
  /api/intake/sessions/{id}/:
    get:
      operationId: intake_sessions_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
      tags:
      - intake
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ClinicalSession'
          description: ''
  /api/intake/sessions/{session_id}/soap/:
    post:
      operationId: intake_sessions_soap_create
      parameters:
      - in: path
        name: session_id
        schema:
          type: integer
        required: true
      tags:
      - intake
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/intake/specialties/:
    get:
      operationId: intake_specialties_list
      description: List all medical specialties
      parameters:
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      tags:
      - intake
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedMedicalSpecialtyList'
          description: ''
  /api/intake/systems/:
    get:
      operationId: intake_systems_list
      description: List all medical systems
      parameters:
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      tags:
      - intake
      security:
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedMedicalSystemList'
          description: ''
  /api/schema/:
    get:
      operationId: schema_retrieve
      description: |-
        OpenApi3 schema for this API. Format can be selected via content negotiation.

        - YAML: application/vnd.oai.openapi
        - JSON: application/vnd.oai.openapi+json
      parameters:
      - in: query
        name: format
        schema:
          type: string
          enum:
          - json
          - yaml
      - in: query
        name: lang
        schema:
          type: string
          enum:
          - af
          - ar
          - ar-dz
          - ast
          - az
          - be
          - bg
          - bn
          - br
          - bs
          - ca
          - ckb
          - cs
          - cy
          - da
          - de
          - dsb
          - el
          - en
          - en-au
          - en-gb
          - eo
          - es
          - es-ar
          - es-co
          - es-mx
          - es-ni
          - es-ve
          - et
          - eu
          - fa
          - fi
          - fr
          - fy
          - ga
          - gd
          - gl
          - he
          - hi
          - hr
          - hsb
          - hu
          - hy
          - ia
          - id
          - ig
          - io
          - is
          - it
          - ja
          - ka
          - kab
          - kk
          - km
          - kn
          - ko
          - ky
          - lb
          - lt
          - lv
          - mk
          - ml
          - mn
          - mr
          - ms
          - my
          - nb
          - ne
          - nl
          - nn
          - os
          - pa
          - pl
          - pt
          - pt-br
          - ro
          - ru
          - sk
          - sl
          - sq
          - sr
          - sr-latn
          - sv
          - sw
          - ta
          - te
          - tg
          - th
          - tk
          - tr
          - tt
          - udm
          - ug
          - uk
          - ur
          - uz
          - vi
          - zh-hans
          - zh-hant
      tags:
      - schema
      security:
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/vnd.oai.openapi:
              schema:
                type: object
                additionalProperties: {}
            application/yaml:
              schema:
                type: object
                additionalProperties: {}
            application/vnd.oai.openapi+json:
              schema:
                type: object
                additionalProperties: {}
            application/json:
              schema:
                type: object
                additionalProperties: {}
          description: ''
components:
  schemas:
    Appointment:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        patient_details:
          allOf:
          - $ref: '#/components/schemas/PatientProfile'
          readOnly: true
        doctor_details:
          allOf:
          - $ref: '#/components/schemas/DoctorProfile'
          readOnly: true
        appointment_date:
          type: string
          format: date
        appointment_time:
          type: string
          format: time
        duration_minutes:
          type: integer
          maximum: 2147483647
          minimum: -2147483648
        status:
          $ref: '#/components/schemas/AppointmentStatusEnum'
        reason:
          type: string
        notes:
          type: string
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        patient:
          type: integer
        doctor:
          type: integer
        clinic:
          type: integer
          nullable: true
        clinical_session:
          type: integer
          nullable: true
      required:
      - appointment_date
      - appointment_time
      - created_at
      - doctor
      - doctor_details
      - id
      - patient
      - patient_details
      - updated_at
    AppointmentStatusEnum:
      enum:
      - scheduled
      - confirmed
      - in_progress
      - completed
      - cancelled
      - no_show
      type: string
      description: |-
        * `scheduled` - Scheduled
        * `confirmed` - Confirmed
        * `in_progress` - In Progress
        * `completed` - Completed
        * `cancelled` - Cancelled
        * `no_show` - No Show
    Clinic:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        name:
          type: string
          maxLength: 200
        address:
          type: string
        city:
          type: string
          maxLength: 100
        country:
          type: string
          maxLength: 100
        phone:
          type: string
          maxLength: 15
        email:
          type: string
          format: email
          maxLength: 254
        registration_number:
          type: string
          maxLength: 50
        is_active:
          type: boolean
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        admin:
          type: integer
          nullable: true
        doctors:
          type: array
          items:
            type: integer
      required:
      - address
      - city
      - created_at
      - doctors
      - email
      - id
      - name
      - phone
      - registration_number
      - updated_at
    ClinicalSession:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        patient:
          type: integer
        patient_name:
          type: string
          readOnly: true
        doctor:
          type: integer
        doctor_name:
          type: string
          readOnly: true
        session_date:
          type: string
          format: date-time
          readOnly: true
        status:
          $ref: '#/components/schemas/ClinicalSessionStatusEnum'
        audio_file:
          type: string
          format: uri
          nullable: true
        audio_duration:
          type: integer
          maximum: 2147483647
          minimum: -2147483648
          nullable: true
          description: Duration in seconds
        raw_transcript:
          type: string
        processed_data: {}
        idiom_detections:
          type: array
          items:
            $ref: '#/components/schemas/IdiomDetectionResult'
          readOnly: true
        ai_provider_used:
          type: string
          maxLength: 50
        confidence_score:
          type: number
          format: double
          nullable: true
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
      required:
      - created_at
      - doctor
      - doctor_name
      - id
      - idiom_detections
      - patient
      - patient_name
      - session_date
      - updated_at
    ClinicalSessionStatusEnum:
      enum:
      - pending
      - processing
      - completed
      - failed
      type: string
      description: |-
        * `pending` - Pending
        * `processing` - Processing
        * `completed` - Completed
        * `failed` - Failed
    ClinicalTerm:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        term:
          type: string
          description: Clinical term in English
          maxLength: 200
        description:
          type: string
          description: Clinical description of the term
        system_name:
          type: string
          readOnly: true
        specialty_name:
          type: string
          readOnly: true
        created_at:
          type: string
          format: date-time
          readOnly: true
      required:
      - created_at
      - id
      - specialty_name
      - system_name
      - term
    Consultation:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        prescriptions:
          type: array
          items:
            $ref: '#/components/schemas/Prescription'
          readOnly: true
        appointment_details:
          allOf:
          - $ref: '#/components/schemas/Appointment'
          readOnly: true
        vital_signs: {}
        physical_exam:
          type: string
        diagnosis:
          type: string
        treatment_plan:
          type: string
        lab_orders: {}
        follow_up_date:
          type: string
          format: date
          nullable: true
        doctor_notes:
          type: string
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        appointment:
          type: integer
        clinical_session:
          type: integer
      required:
      - appointment
      - appointment_details
      - clinical_session
      - created_at
      - diagnosis
      - id
      - prescriptions
      - treatment_plan
      - updated_at
    DoctorProfile:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        license_number:
          type: string
          maxLength: 50
        specialization:
          type: string
          maxLength: 100
        qualifications:
          type: string
        experience_years:
          type: integer
          maximum: 2147483647
          minimum: -2147483648
        clinic_name:
          type: string
          maxLength: 200
        clinic_address:
          type: string
        consultation_fee:
          type: string
          format: decimal
          pattern: ^-?\d{0,8}(?:\.\d{0,2})?$
          nullable: true
        available_days: {}
        available_time_start:
          type: string
          format: time
          nullable: true
        available_time_end:
          type: string
          format: time
          nullable: true
        is_verified:
          type: boolean
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        user:
          type: integer
      required:
      - clinic_address
      - clinic_name
      - created_at
      - experience_years
      - id
      - license_number
      - qualifications
      - specialization
      - updated_at
      - user
    IdiomDetectionResult:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        idiom_text:
          type: string
          readOnly: true
        clinical_terms:
          type: string
          readOnly: true
        risk_note:
          type: string
          readOnly: true
        matched_text:
          type: string
          description: The exact text that matched the idiom
          maxLength: 500
        created_at:
          type: string
          format: date-time
          readOnly: true
      required:
      - clinical_terms
      - created_at
      - id
      - idiom_text
      - matched_text
      - risk_note
    MedicalSpecialty:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        name:
          type: string
          maxLength: 100
        system_name:
          type: string
          readOnly: true
        description:
          type: string
        created_at:
          type: string
          format: date-time
          readOnly: true
      required:
      - created_at
      - id
      - name
      - system_name
    MedicalSystem:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        name:
          $ref: '#/components/schemas/NameEnum'
        description:
          type: string
        created_at:
          type: string
          format: date-time
          readOnly: true
      required:
      - created_at
      - id
      - name
    NameEnum:
      enum:
      - cardiovascular
      - respiratory
      - gastrointestinal
      - neurological
      - musculoskeletal
      - integumentary
      - endocrine
      - genitourinary
      - reproductive
      - psychiatric
      - hematologic
      - immunologic
      - renal
      - hepatic
      - ophthalmic
      - otolaryngologic
      - dental
      type: string
      description: |-
        * `cardiovascular` - Cardiovascular System
        * `respiratory` - Respiratory System
        * `gastrointestinal` - Gastrointestinal System
        * `neurological` - Neurological System
        * `musculoskeletal` - Musculoskeletal System
        * `integumentary` - Integumentary System (Skin)
        * `endocrine` - Endocrine System
        * `genitourinary` - Genitourinary System
        * `reproductive` - Reproductive System
        * `psychiatric` - Psychiatric/Mental Health
        * `hematologic` - Hematologic System
        * `immunologic` - Immunologic System
        * `renal` - Renal/Urinary System
        * `hepatic` - Hepatic/Liver System
        * `ophthalmic` - Ophthalmic/Eye System
        * `otolaryngologic` - Otolaryngologic/ENT System
        * `dental` - Dental/Oral System
    PaginatedAppointmentList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/Appointment'
    PaginatedClinicList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/Clinic'
    PaginatedClinicalSessionList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/ClinicalSession'
    PaginatedMedicalSpecialtyList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/MedicalSpecialty'
    PaginatedMedicalSystemList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/MedicalSystem'
    PaginatedPatientIdiomList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/PatientIdiom'
    PatchedAppointment:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        patient_details:
          allOf:
          - $ref: '#/components/schemas/PatientProfile'
          readOnly: true
        doctor_details:
          allOf:
          - $ref: '#/components/schemas/DoctorProfile'
          readOnly: true
        appointment_date:
          type: string
          format: date
        appointment_time:
          type: string
          format: time
        duration_minutes:
          type: integer
          maximum: 2147483647
          minimum: -2147483648
        status:
          $ref: '#/components/schemas/AppointmentStatusEnum'
        reason:
          type: string
        notes:
          type: string
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        patient:
          type: integer
        doctor:
          type: integer
        clinic:
          type: integer
          nullable: true
        clinical_session:
          type: integer
          nullable: true
    PatchedClinic:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        name:
          type: string
          maxLength: 200
        address:
          type: string
        city:
          type: string
          maxLength: 100
        country:
          type: string
          maxLength: 100
        phone:
          type: string
          maxLength: 15
        email:
          type: string
          format: email
          maxLength: 254
        registration_number:
          type: string
          maxLength: 50
        is_active:
          type: boolean
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        admin:
          type: integer
          nullable: true
        doctors:
          type: array
          items:
            type: integer
    PatchedConsultation:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        prescriptions:
          type: array
          items:
            $ref: '#/components/schemas/Prescription'
          readOnly: true
        appointment_details:
          allOf:
          - $ref: '#/components/schemas/Appointment'
          readOnly: true
        vital_signs: {}
        physical_exam:
          type: string
        diagnosis:
          type: string
        treatment_plan:
          type: string
        lab_orders: {}
        follow_up_date:
          type: string
          format: date
          nullable: true
        doctor_notes:
          type: string
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        appointment:
          type: integer
        clinical_session:
          type: integer
    PatchedDoctorProfile:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        license_number:
          type: string
          maxLength: 50
        specialization:
          type: string
          maxLength: 100
        qualifications:
          type: string
        experience_years:
          type: integer
          maximum: 2147483647
          minimum: -2147483648
        clinic_name:
          type: string
          maxLength: 200
        clinic_address:
          type: string
        consultation_fee:
          type: string
          format: decimal
          pattern: ^-?\d{0,8}(?:\.\d{0,2})?$
          nullable: true
        available_days: {}
        available_time_start:
          type: string
          format: time
          nullable: true
        available_time_end:
          type: string
          format: time
          nullable: true
        is_verified:
          type: boolean
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        user:
          type: integer
    PatchedPatientProfile:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        blood_group:
          type: string
          maxLength: 5
        allergies:
          type: string
        chronic_conditions:
          type: string
        current_medications:
          type: string
        emergency_contact_name:
          type: string
          maxLength: 100
        emergency_contact_phone:
          type: string
          maxLength: 15
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        user:
          type: integer
        preferred_doctor:
          type: integer
          nullable: true
    PatchedUser:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        password:
          type: string
          maxLength: 128
        last_login:
          type: string
          format: date-time
          nullable: true
        is_superuser:
          type: boolean
          title: Superuser status
          description: Designates that this user has all permissions without explicitly
            assigning them.
        username:
          type: string
          description: Required. 150 characters or fewer. Letters, digits and @/./+/-/_
            only.
          pattern: ^[\w.@+-]+$
          maxLength: 150
        first_name:
          type: string
          maxLength: 150
        last_name:
          type: string
          maxLength: 150
        email:
          type: string
          format: email
          title: Email address
          maxLength: 254
        is_staff:
          type: boolean
          title: Staff status
          description: Designates whether the user can log into this admin site.
        is_active:
          type: boolean
          title: Active
          description: Designates whether this user should be treated as active. Unselect
            this instead of deleting accounts.
        date_joined:
          type: string
          format: date-time
        user_type:
          $ref: '#/components/schemas/UserTypeEnum'
        phone_number:
          type: string
          maxLength: 15
        profile_picture:
          type: string
          format: uri
          nullable: true
        date_of_birth:
          type: string
          format: date
          nullable: true
        address:
          type: string
        city:
          type: string
          maxLength: 100
        country:
          type: string
          maxLength: 100
        preferred_language:
          type: string
          maxLength: 10
        email_verified:
          type: boolean
        phone_verified:
          type: boolean
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        groups:
          type: array
          items:
            type: integer
          description: The groups this user belongs to. A user will get all permissions
            granted to each of their groups.
        user_permissions:
          type: array
          items:
            type: integer
          description: Specific permissions for this user.
    PatientIdiom:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        clinical_terms:
          type: array
          items:
            $ref: '#/components/schemas/ClinicalTerm'
          readOnly: true
        clinical_term_ids:
          type: array
          items:
            type: integer
            writeOnly: true
          writeOnly: true
        idiom:
          type: string
          maxLength: 500
        language:
          type: string
          maxLength: 10
        confidence_weight:
          type: number
          format: double
        context_notes:
          type: string
          description: Notes on when/how this idiom is used
        region:
          type: string
          description: Region where this idiom is common
          maxLength: 100
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        clinical_term:
          type: integer
          nullable: true
        symptom:
          type: integer
          nullable: true
        medical_system:
          type: integer
          nullable: true
        medical_specialty:
          type: integer
          nullable: true
      required:
      - clinical_terms
      - created_at
      - id
      - idiom
      - updated_at
    PatientProfile:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        blood_group:
          type: string
          maxLength: 5
        allergies:
          type: string
        chronic_conditions:
          type: string
        current_medications:
          type: string
        emergency_contact_name:
          type: string
          maxLength: 100
        emergency_contact_phone:
          type: string
          maxLength: 15
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        user:
          type: integer
        preferred_doctor:
          type: integer
          nullable: true
      required:
      - created_at
      - id
      - updated_at
      - user
    Prescription:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        medication_name:
          type: string
          maxLength: 200
        dosage:
          type: string
          maxLength: 100
        frequency:
          type: string
          maxLength: 100
        duration:
          type: string
          maxLength: 100
        instructions:
          type: string
        refills:
          type: integer
          maximum: 2147483647
          minimum: -2147483648
        created_at:
          type: string
          format: date-time
          readOnly: true
        consultation:
          type: integer
      required:
      - consultation
      - created_at
      - dosage
      - duration
      - frequency
      - id
      - medication_name
    Register:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        password:
          type: string
          maxLength: 128
        last_login:
          type: string
          format: date-time
          nullable: true
        is_superuser:
          type: boolean
          title: Superuser status
          description: Designates that this user has all permissions without explicitly
            assigning them.
        username:
          type: string
          description: Required. 150 characters or fewer. Letters, digits and @/./+/-/_
            only.
          pattern: ^[\w.@+-]+$
          maxLength: 150
        first_name:
          type: string
          maxLength: 150
        last_name:
          type: string
          maxLength: 150
        email:
          type: string
          format: email
          title: Email address
          maxLength: 254
        is_staff:
          type: boolean
          title: Staff status
          description: Designates whether the user can log into this admin site.
        is_active:
          type: boolean
          title: Active
          description: Designates whether this user should be treated as active. Unselect
            this instead of deleting accounts.
        date_joined:
          type: string
          format: date-time
        user_type:
          $ref: '#/components/schemas/UserTypeEnum'
        phone_number:
          type: string
          maxLength: 15
        profile_picture:
          type: string
          format: uri
          nullable: true
        date_of_birth:
          type: string
          format: date
          nullable: true
        address:
          type: string
        city:
          type: string
          maxLength: 100
        country:
          type: string
          maxLength: 100
        preferred_language:
          type: string
          maxLength: 10
        email_verified:
          type: boolean
        phone_verified:
          type: boolean
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        groups:
          type: array
          items:
            type: integer
          description: The groups this user belongs to. A user will get all permissions
            granted to each of their groups.
        user_permissions:
          type: array
          items:
            type: integer
          description: Specific permissions for this user.
      required:
      - created_at
      - id
      - password
      - phone_number
      - updated_at
      - username
    User:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        password:
          type: string
          maxLength: 128
        last_login:
          type: string
          format: date-time
          nullable: true
        is_superuser:
          type: boolean
          title: Superuser status
          description: Designates that this user has all permissions without explicitly
            assigning them.
        username:
          type: string
          description: Required. 150 characters or fewer. Letters, digits and @/./+/-/_
            only.
          pattern: ^[\w.@+-]+$
          maxLength: 150
        first_name:
          type: string
          maxLength: 150
        last_name:
          type: string
          maxLength: 150
        email:
          type: string
          format: email
          title: Email address
          maxLength: 254
        is_staff:
          type: boolean
          title: Staff status
          description: Designates whether the user can log into this admin site.
        is_active:
          type: boolean
          title: Active
          description: Designates whether this user should be treated as active. Unselect
            this instead of deleting accounts.
        date_joined:
          type: string
          format: date-time
        user_type:
          $ref: '#/components/schemas/UserTypeEnum'
        phone_number:
          type: string
          maxLength: 15
        profile_picture:
          type: string
          format: uri
          nullable: true
        date_of_birth:
          type: string
          format: date
          nullable: true
        address:
          type: string
        city:
          type: string
          maxLength: 100
        country:
          type: string
          maxLength: 100
        preferred_language:
          type: string
          maxLength: 10
        email_verified:
          type: boolean
        phone_verified:
          type: boolean
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        groups:
          type: array
          items:
            type: integer
          description: The groups this user belongs to. A user will get all permissions
            granted to each of their groups.
        user_permissions:
          type: array
          items:
            type: integer
          description: Specific permissions for this user.
      required:
      - created_at
      - id
      - password
      - phone_number
      - updated_at
      - username
    UserTypeEnum:
      enum:
      - patient
      - doctor
      - clinic_admin
      - super_admin
      type: string
      description: |-
        * `patient` - Patient
        * `doctor` - Doctor
        * `clinic_admin` - Clinic Admin
        * `super_admin` - Super Admin
  securitySchemes:
    cookieAuth:
      type: apiKey
      in: cookie
      name: sessionid
    tokenAuth:
      type: apiKey
      in: header
      name: Authorization
      description: Token-based authentication with required prefix "Token"
