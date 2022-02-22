import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy import Text, String, Boolean, Date, DateTime, Numeric, Integer, Time, Float, DECIMAL, Text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

#! YUNG USER TABLE (AND PROFILES/ROLES) WAG MUNA DITO

#** CORE
#? VISITOR MANAGEMENT
class Station(Base):
    __tablename__ = 'stations'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)

    appointment = relationship('Appointment', back_populates='station')

class Health_Form(Base):
    __tablename__ = 'health_forms'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    symptoms = Column(String(255), nullable=True)
    condition = Column(String(255), nullable=False)
    date_submitted = Column(Date, nullable=False, default=Text('NOW()'))

    user = relationship('User', back_populates='health_form')
    health_pass = relationship('Pass', back_populates='health_form')

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    station_id = Column(String(36), ForeignKey('stations.id'), nullable=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    contact_number = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    address = Column(String(255), nullable=False)
    patient_name = Column(String(255), nullable=True)
    purpose = Column(String(255), nullable=False)
    schedule = Column(Date, nullable=False)
    status = Column(String(255), default='Pending')
    date_submitted = Column(Date, nullable=False)
    type = Column(String(255), nullable=False)
    file = Column(String(255), nullable=True)
    remarks = Column(Text, nullable=True)
    is_allowed = Column(Boolean, nullable=True)

    user = relationship('User', back_populates='appointment')
    station = relationship('Station', back_populates='appointment')
    appointment_pass = relationship('Pass', back_populates='appointment')
    health_form = relationship('Health_Form', secondary='join(Health_Form, Pass, Pass.health_form_id == Health_Form.id)', secondaryjoin='Health_Form.id == Pass.health_form_id', uselist=False, viewonly=True)
    visit = relationship('Visit', secondary='join(Pass, Visit, Visit.pass_id == Pass.id)', secondaryjoin='Pass.id == Visit.pass_id', uselist=False, viewonly=True)

class Pass(Base):
    __tablename__ = 'passes'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    appointment_id = Column(String(36), ForeignKey('appointments.id'), nullable=True)
    health_form_id = Column(String(36), ForeignKey('health_forms.id'), nullable=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    user = relationship('User', back_populates='user_pass')
    appointment = relationship('Appointment', back_populates='appointment_pass')
    health_form = relationship('Health_Form', back_populates='health_pass')
    visit = relationship('Visit', back_populates='visit_pass')

class Visit(Base):
    __tablename__ = 'visits'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    pass_id = Column(String(36), ForeignKey('passes.id'), nullable=True)
    image = Column(String(255), nullable=False)
    remarks = Column(Text, nullable=False)
    check_in = Column(DateTime, default=Text('NOW()'))
    check_out = Column(DateTime, nullable=True)

    visit_pass = relationship('Pass', back_populates='visit')
    appointment = relationship('Appointment', secondary='join(Pass, Appointment, Pass.appointment_id == Appointment.id)', secondaryjoin='Appointment.id == Pass.appointment_id', uselist=False, viewonly=True)
    health_form = relationship('Health_Form', secondary='join(Pass, Health_Form, Pass.health_form_id == Health_Form.id)', secondaryjoin='Health_Form.id == Pass.health_form_id', uselist=False, viewonly=True)
    user = relationship('User', secondary='join(Pass, User, Pass.user_id == User.id)', secondaryjoin='User.id == Pass.user_id', uselist=False, viewonly=True)

class Visit_Blacklist(Base):
    __tablename__ = 'blacklists'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    image = Column(String(255), nullable=True)
    remarks = Column(Text, nullable=False)
    is_active = Column(Boolean, default=Text('1'))
    is_seen = Column(Boolean, default=Text('0'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    user = relationship('User', back_populates='blacklist', uselist=False)
    profile = relationship('User_Profile', secondary='join(User, User_Profile, User.id == User_Profile.user_id)', secondaryjoin='User_Profile.user_id == User.id', viewonly=True, uselist=False)

#? TREATMENT MANAGEMENT
class InPatient(Base):
    __tablename__ = "inpatients"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
    suffix_name = Column(String(100))
    birth_date = Column(Date)
    gender = Column(String(100))
    contact_no = Column(String(15))
    email = Column(String(100), unique=True)
    blood_type = Column(String(10))
    picture = Column(String(255))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))


    surgeries = relationship('Surgery', back_populates='inpatient')
    treatments = relationship('Treatment', back_populates='inpatient')
    lab_requests = relationship('LabRequest', back_populates='inpatient')

class LabRequest(Base):
    __tablename__ = "lab_requests"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    lab_test_id = Column(String(36), ForeignKey("lab_tests.id"))
    # lab_result_id = Column(String(36), ForeignKey("lab_results.id"))
    inpatient_id = Column(String(36), ForeignKey("inpatients.id"))
    outpatient_id = Column(String(36), ForeignKey("outpatients.id"))
    quantity = Column(Numeric(15,2), nullable=False)

    lab_request_no = Column(String(100))

    is_active = Column(String(100), default='ACTIVE')
    status = Column(String(100), default='PENDING')
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))


    lab_result = relationship('LabResult', back_populates='lab_request')
    lab_test = relationship('LabTest', back_populates='lab_requests')

    inpatient = relationship('InPatient', back_populates='lab_requests')
    outpatient = relationship('OutPatient', back_populates='lab_requests')

#* used by: MRS
class LabResult(Base):
    __tablename__ = "lab_results"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    lab_request_id = Column(String(36), ForeignKey("lab_requests.id"))
    specimen = Column(String(100))
    result = Column(Text)
    reference = Column(String(100))
    unit = Column(String(100))
    detailed_result = Column(String(100))
    
    comments = Column(String(255))

    ordered = Column(String(150))
    dt_requested = Column(DateTime)
    dt_received = Column(DateTime)
    dt_reported = Column(DateTime)


    status = Column(String(100), default='PROCESSING')
    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))


    lab_request = relationship('LabRequest', back_populates='lab_result')

class LabTest(Base):
    __tablename__ = "lab_tests"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    name = Column(String(100), unique=True)
    description = Column(Text)
    fee = Column(Numeric(15,2))

    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    lab_requests = relationship('LabRequest', back_populates='lab_test')

class OutPatient(Base):
    __tablename__ = "outpatients"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
    suffix_name = Column(String(100))
    birth_date = Column(Date)
    gender = Column(String(100))
    contact_no = Column(String(15))
    email = Column(String(100), unique=True)
    blood_type = Column(String(10))
    picture = Column(String(255))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))


    treatments = relationship('Treatment', back_populates='outpatient')
    lab_requests = relationship('LabRequest', back_populates='outpatient')

class SurgeryInCharge(Base):
    __tablename__ = "surgery_in_charge"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    professional_fee = Column(Numeric(15,2))


    in_charge_id = Column(ForeignKey('users.id'))
    surgery_id = Column(ForeignKey('surgeries.id'))

    in_charge = relationship('User', back_populates="handled_surgeries")
    surgery = relationship("Surgery", back_populates="in_charge")

class SurgeryType(Base):
    __tablename__ = "surgery_types"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    name = Column(String(100), unique=True)
    description = Column(Text)
    price = Column(Numeric(15,2))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))


    surgeries = relationship("Surgery", back_populates="surgery_type")

class Surgery(Base):
    __tablename__ = "surgeries"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    surgery_no = Column(String(100))
    inpatient_id = Column(String(36), ForeignKey("inpatients.id"))

    room = Column(String(100))

    surgery_type_id = Column(String(36), ForeignKey("surgery_types.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    head_surgeon_id = Column(String(36), ForeignKey("users.id"))
    description = Column(String(255))

    is_active = Column(String(100), default='ACTIVE')
    status = Column(String(100), default='PENDING')
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))


    inpatient = relationship('InPatient', back_populates='surgeries')
    surgery_type = relationship("SurgeryType", back_populates="surgeries")

    in_charge = relationship('SurgeryInCharge', back_populates="surgery")

class TreatmentType(Base):
    __tablename__ = "treatment_types"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    name = Column(String(100), unique=True)
    room = Column(String(100))
    description = Column(Text)
    fee = Column(Numeric(15,2))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))


    treatments = relationship('Treatment', back_populates='treatment_type')

class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    treatment_no = Column(String(100))
    room = Column(String(100))
    quantity = Column(Numeric(15,2), nullable=False)
    inpatient_id = Column(String(36), ForeignKey("inpatients.id"))
    outpatient_id = Column(String(36), ForeignKey("outpatients.id"))
    treatment_type_id = Column(String(36), ForeignKey("treatment_types.id"))
    physician_id = Column(String(36), ForeignKey("users.id")) # DOCTOR IN CHARGE
    description = Column(Text)

    professional_fee = Column(Numeric(15,2))
    session_no = Column(Text)
    session_DateTime = Column(DateTime)
    drug = Column(Text)
    dose = Column(Text)
    next_schedule = Column(DateTime)
    comments = Column(Text)
    


    status = Column(String(100), default='PENDING')
    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))


    inpatient = relationship('InPatient', back_populates='treatments')
    outpatient = relationship('OutPatient', back_populates='treatments')
    physician = relationship('User', back_populates='treatments')
    treatment_type = relationship('TreatmentType', back_populates='treatments')

#? MEDICAL RECORDS
class Doctor(Base):
    __tablename__ = 'doctors'

    doc_id          = Column(String(36), primary_key=True, default=Text('UUID()'))
    first_name      = Column(String(255), nullable=False)
    middle_name     = Column(String(255), nullable=True)
    last_name       = Column(String(255), nullable=False)
    department      = Column(String(255), nullable=False)
    contact_number  = Column(String(255), nullable=False)
    region          = Column(String(255), nullable=False)
    street          = Column(String(255), nullable=False)
    barangay        = Column(String(255), nullable=False)
    municipality    = Column(String(255), nullable=False)
    province        = Column(String(255), nullable=False)
    active_status   = Column(String(255), nullable=False, default="Active")
    created_at      = Column(DateTime, default=Text('NOW()'))
    updated_at      = Column(DateTime, onupdate=Text('NOW()'))

    diagnosisdocFK        = relationship('Diagnosis', back_populates="docdiagnosisFK")
    progressnoteFK        = relationship('ProgressNote', back_populates="docentryFK")
    doctorprescriptionFK  = relationship('Prescription', back_populates="docprescriptionFK")   

    doctor_profilesFK    = relationship('UserProfile', back_populates='docProfileFK')

class Patient(Base):
    __tablename__ = 'patients'

    patient_id      = Column(String(36), primary_key=True, default=Text('UUID()'))
    first_name      = Column(String(255), nullable=False)
    middle_name     = Column(String(255), nullable=True)
    last_name       = Column(String(255), nullable=False)
    gender          = Column(String(255), nullable=False)
    birth_date      = Column(Date, nullable=False)
    contact_number  = Column(String(255), nullable=False)
    region          = Column(String(255), nullable=False)
    street          = Column(String(255), nullable=False)
    barangay        = Column(String(255), nullable=False)
    municipality    = Column(String(255), nullable=False)
    province        = Column(String(255), nullable=False)
    weight          = Column(String(255), nullable=False)
    height          = Column(String(255), nullable=False)
    blood_type      = Column(String(255), nullable=False)
    guardian        = Column(String(255), nullable=False)
    active_status   = Column(String(255), nullable=False, default="Active")
    created_at      = Column(DateTime, default=Text('NOW()'))
    updated_at      = Column(DateTime, onupdate=Text('NOW()'))

    patientFK             = relationship('Record', back_populates="patientrecordFK")
    patientdischargeFK    = relationship('Discharge', back_populates="dischargeFK")

    patient_profilesFK    = relationship('UserProfile', back_populates='patientProfileFK')
    patientrequestFK      = relationship('Request', back_populates='requesterFK')

    historyrecordFK         = relationship('History', back_populates="historyFK")

class Record(Base):
    __tablename__ = 'patient_records'

    patient_record_id       = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_id              = Column(String(36), ForeignKey('patients.patient_id'))
    # record_id               = Column(String(8), default=base64.b64encode(os.urandom(6)).decode('ascii'))
    # record_id               = Column(String(8), default=Text('UUID()'))
    created_at              = Column(DateTime, default=Text('NOW()'))
    updated_at              = Column(DateTime, onupdate=Text('NOW()'))


    # created_byFK            = relationship('User', back_populates="byusersFK")
    patientrecordFK         = relationship('Patient', back_populates="patientFK")

    # historyrecordFK         = relationship('History', back_populates="historyFK")
    problemrecordFK         = relationship('Problem', back_populates="problemFK")
    diagnosisrecordFK       = relationship('Diagnosis', back_populates="diagnosisrecFK")
    labresultrecordFK       = relationship('LabResult', back_populates="labresultFK")
    prescriptionrecordFK    = relationship('Prescription', back_populates="prescriptionsFK")
    progressnoterecordFK    = relationship('ProgressNote', back_populates="progressnoteFK")

    record_allergyFK        = relationship('Allergy', back_populates="allergiesFK")
    record_immunizationFK   = relationship('Immunization', back_populates="immunizationsFK")
    record_medicationFK     = relationship('Medication', back_populates="medicationsFK")
    record_attachmentFK     = relationship('Attachment', back_populates="attachmentsFK")

    call_logrecordFK        = relationship('CallLog', back_populates="call_logFK")

class History(Base):
    __tablename__ = 'medical_history'

    history_id              = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_id              = Column(String(36), ForeignKey('patients.patient_id'))
    # patient_record_id       = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    chief_complaint         = Column(String(255), nullable=True)
    previous_hospital       = Column(String(255), nullable=True)
    previous_doctor         = Column(String(255), nullable=True)
    previous_diagnosis      = Column(String(255), nullable=True)
    previous_treatment      = Column(String(255), nullable=True)
    previous_surgeries      = Column(String(255), nullable=True)
    previous_medication     = Column(String(255), nullable=True)
    health_conditions       = Column(String(255), nullable=True)
    special_privileges      = Column(String(255), nullable=True)
    family_history          = Column(String(255), nullable=True)
    created_at              = Column(DateTime, default=Text('NOW()'))
    updated_at              = Column(DateTime, onupdate=Text('NOW()'))

    historyFK               = relationship('Patient', back_populates="historyrecordFK")

class Problem(Base):
    __tablename__ = 'problems'

    problem_id              = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id       = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    problem_name            = Column(String(255), nullable=False)
    problem_note            = Column(String(255), nullable=False)
    active_status           = Column(String(255), nullable=False)
    date_occured            = Column(Date, nullable=False)
    date_resolved           = Column(Date, nullable=True)
    created_at              = Column(DateTime, default=Text('NOW()'))
    updated_at              = Column(DateTime, onupdate=Text('NOW()'))
    
    problemFK               = relationship('Record', back_populates="problemrecordFK")

class Diagnosis(Base):
    __tablename__ = 'diagnosis'

    diagnosis_id      = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    doc_id            = Column(String(36), ForeignKey('doctors.doc_id'))
    diagnosis               = Column(String(255), nullable=False)
    description             = Column(String(255), nullable=False)
    

    docdiagnosisFK     = relationship('Doctor', back_populates="diagnosisdocFK")
   #diagnosisFK        = relationship('DiagnosisDetail', back_populates="dianosisdetailFK")
    diagnosisrecFK     = relationship('Record', back_populates="diagnosisrecordFK")

#* used by: TMS
class LabResult(Base):
    __tablename__ = 'lab_results'

    lab_result_id       = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id   = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    specimen            = Column(String(255), nullable=False)
    result              = Column(String(255), nullable=False)
    reference           = Column(String(255), nullable=False)
    unit                = Column(String(255), nullable=False)
    status              = Column(String(255), nullable=False)
    detailed_result     = Column(String(255), nullable=False)

    labresultFK     = relationship('Record', back_populates="labresultrecordFK")

class Prescription(Base):
    __tablename__ = 'prescriptions'

    prescription_id           = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id         = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    medication_name           = Column(String(255), nullable=True)
    medication_type           = Column(String(255), nullable=True)
    dosage                    = Column(String(255), nullable=True)
    quantity                  = Column(String(255), nullable=False)
    frequency                 = Column(String(255), nullable=True)
    med_taken_for             = Column(String(255), nullable=True)
    doc_id                    = Column(String(36), ForeignKey('doctors.doc_id'))
    prescription_notes        = Column(String(255), nullable=False)
    created_at                = Column(DateTime, default=Text('NOW()'))
    updated_at                = Column(DateTime, onupdate=Text('NOW()'))
    

    docprescriptionFK       = relationship('Doctor', back_populates="doctorprescriptionFK")    
    #prescriptiondetailsFK   = relationship('PrescriptionDetail', back_populates="prescribeFK")
    prescriptionsFK         = relationship('Record', back_populates="prescriptionrecordFK")

class ProgressNote(Base):
    __tablename__ = 'progress_notes'

    progress_note_id        = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id       = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    # progress_note_id    =  Column(String(36), ForeignKey('progress_notes.progress_note_id'))
    doc_id                  =  Column(String(36), ForeignKey('doctors.doc_id'))
    reason_for_consultation = Column(String(255), nullable=False)
    physical_examination    = Column(String(255), nullable=False)
    impression              = Column(String(255), nullable=False)
    recommendation          = Column(String(255), nullable=False)
    consultation_date        = Column(Date, nullable=True)
    next_appointment        = Column(Date, nullable=True)
    created_at              = Column(DateTime, default=Text('NOW()'))
    updated_at              = Column(DateTime, onupdate=Text('NOW()'))
    
   # progressdetailFK    = relationship('ProgressNoteDetail', back_populates="progressFK")
    progressnoteFK          = relationship('Record', back_populates="progressnoterecordFK")
    docentryFK              = relationship('Doctor',back_populates="progressnoteFK")

class CallLog(Base):
    __tablename__ = 'patient_call_logs'

    patient_call_log_id     = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id       = Column(String(36), ForeignKey('patient_records.patient_record_id'))

    call_logFK              = relationship('Record', back_populates="call_logrecordFK")
    logsFK                  = relationship('CallLogDetail', back_populates="call_logsFK")

class CallLogDetail(Base):
    __tablename__ = 'patient_call_log_details'

    call_log_detail_id     = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_call_log_id    = Column(String(36), ForeignKey('patient_call_logs.patient_call_log_id'))
    call_log_date          = Column(Date, nullable=False)
    # payor_called           = Column(String(255), nullable=False)
    contact_first_name     = Column(String(255), nullable=False)
    contact_last_name      = Column(String(255), nullable=False)
    contact_phone          = Column(String(255), nullable=False)
    call_details           = Column(String(255), nullable=False)
    follow_up_date         = Column(Date, nullable=True)
    created_at             = Column(DateTime, default=Text('NOW()'))
    updated_at             = Column(DateTime, onupdate=Text('NOW()'))

    call_logsFK            = relationship('CallLog', back_populates="logsFK")

class Allergy(Base):
    __tablename__ = 'allergies'

    allergy_id             = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id      = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    allergen               = Column(String(255), nullable=True)
    reaction               = Column(String(255), nullable=True)
    severity               = Column(String(255), nullable=True)
    comment                = Column(String(255), nullable=True)
    created_at             = Column(DateTime, default=Text('NOW()'))
    updated_at             = Column(DateTime, onupdate=Text('NOW()'))

    allergiesFK            = relationship('Record', back_populates="record_allergyFK")

class Immunization(Base):
    __tablename__ = 'immunizations'

    immunization_id        = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id      = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    vaccine                = Column(String(255), nullable=True)
    type                   = Column(String(255), nullable=True)
    date_given             = Column(Date, nullable=True)
    administered_by        = Column(String(255), nullable=True)
    created_at             = Column(DateTime, default=Text('NOW()'))
    updated_at             = Column(DateTime, onupdate=Text('NOW()'))

    immunizationsFK        = relationship('Record', back_populates="record_immunizationFK")

class Medication(Base):
    __tablename__ = 'medications'

    medication_id          = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id      = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    drug_name              = Column(String(255), nullable=True)
    dosage                 = Column(String(255), nullable=True)
    route                  = Column(String(255), nullable=True)
    frequency              = Column(String(255), nullable=True)
    quantity               = Column(String(255), nullable=True)
    refill                 = Column(String(255), nullable=True)
    instructions           = Column(String(255), nullable=True)
    start_date             = Column(Date, nullable=True)
    end_date               = Column(Date, nullable=True)
    medication_status      = Column(String(255), nullable=True, default="Active")
    created_at             = Column(DateTime, default=Text('NOW()'))
    updated_at             = Column(DateTime, onupdate=Text('NOW()'))

    medicationsFK          = relationship('Record', back_populates="record_medicationFK")

class Attachment(Base):
    __tablename__ = 'attachments'

    attachment_id          = Column(String(36), primary_key=True, default=Text('UUID()'))
    patient_record_id      = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    attachment             = Column(String(255), nullable=True)
    type                   = Column(String(255), nullable=True)
    created_at             = Column(DateTime, default=Text('NOW()'))
    updated_at             = Column(DateTime, onupdate=Text('NOW()'))

    attachmentsFK          = relationship('Record', back_populates="record_attachmentFK")

class Request(Base):
    __tablename__ = 'requests'

    request_id              = Column(String(36), primary_key=True, default=Text('UUID()'))
    review_by               = Column(String(36), ForeignKey('users.user_id'))
    patient_id              = Column(String(36), ForeignKey('patients.patient_id'))
    request_information     = Column(String(255), nullable=True)
    disclosure_reason       = Column(String(255), nullable=True)
    delivery                = Column(String(255), nullable=True)
    email                   = Column(String(255), nullable=True)
    requested_file          = Column(String(255), nullable=True)
    review_reason           = Column(String(255), nullable=True)
    active_status           = Column(String(255), nullable=False, default="Pending")
    created_at              = Column(DateTime, nullable=True, default=Text('NOW()'))
    updated_at              = Column(DateTime, nullable=True, onupdate=Text('NOW()'))

    reviewbyFK = relationship('User', back_populates='requestreviewFK')
    requesterFK = relationship('Patient', back_populates='patientrequestFK')

#*-----end of core------

#** FINANCE
#*-----end of finance-----

#** HUMAR RESOURCE
#? TIME AND ATTENDANCE
class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    employee_id = Column(String(36), ForeignKey('employees.id'), nullable=False)
    time_in_id = Column(String(36), ForeignKey('time_ins.id'), nullable=False)
    time_out_id = Column(String(36), ForeignKey('time_outs.id'), nullable=False)
    hours_worked = Column(String(36), nullable=False)
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    employees = relationship('Employee', back_populates='attendances', lazy='joined')
    time_ins = relationship('TimeIn', back_populates='attendances', lazy='joined')
    time_outs = relationship('TimeOut', back_populates='attendances', lazy='joined')

#! PAKIAYOS HEHE
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    employee_type_id = Column(Integer, ForeignKey('employee_types.id'), nullable=True)
    employee_status_id = Column(Integer, ForeignKey('employee_status.id'), nullable=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    shift_type_id = Column(Integer, ForeignKey('shift_types.id'), nullable=True)
    attendance_status = Column(String(255), nullable=True)
    monday = Column(String(255), nullable=True)
    tuesday = Column(String(255), nullable=True)
    wednesday = Column(String(255), nullable=True)
    thursday = Column(String(255), nullable=True)
    friday = Column(String(255), nullable=True)
    saturday = Column(String(255), nullable=True)
    sunday = Column(String(255), nullable=True)
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    users = relationship('User', back_populates='employees', lazy='joined')
    employee_types = relationship('EmployeeType', back_populates='employees', lazy='joined')
    employee_status = relationship('EmployeeStatus', back_populates='employees', lazy='joined')
    shift_types = relationship('ShiftType', back_populates='employees', lazy='joined')
    time_ins = relationship('TimeIn', back_populates='employees')
    time_outs = relationship('TimeOut', back_populates='employees')
    attendances = relationship('Attendance', back_populates='employees')
    leaves = relationship('Leave', back_populates='employees')
    missed_times = relationship('MissedTime', back_populates='employees')
    shift_changes = relationship('ShiftChange', back_populates='employees')

class EmployeeStatus(Base):
    __tablename__ = 'employee_status'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    title = Column(String(255), nullable=False)
    number_of_days = Column(String(255), nullable=False)
    active_status = Column(String(255), nullable=True, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    employees = relationship('Employee', back_populates='employee_status')

#* used by: Procurement
class EmployeeType(Base):
    __tablename__ = 'employee_types'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    title = Column(String(255), nullable=False)
    active_status = Column(String(255), nullable=True, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    employees = relationship('Employee', back_populates='employee_types')

class Leave(Base):
    __tablename__ = 'leaves'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    employee_id = Column(String(36), ForeignKey('employees.id'), nullable=False)
    leave_type_id = Column(String(36), ForeignKey('leave_types.id'), nullable=False)
    leave_sub_type_id = Column(String(36), ForeignKey('leave_sub_types.id'), nullable=False)
    title = Column(String(255), nullable=False)
    reason = Column(String(500), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(255), nullable=False, server_default=Text("'Pending'"))
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    leave_types = relationship('LeaveType', back_populates='leaves', lazy='joined')
    employees = relationship('Employee', back_populates='leaves', lazy='joined')
    leave_sub_types = relationship('LeaveSubType', back_populates='leaves', lazy='joined')

class LeaveSubType(Base):
    __tablename__ = 'leave_sub_types'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    title = Column(String(255), nullable=False)
    number_of_days = Column(String(255), nullable=False)
    leave_type_id = Column(String(36), ForeignKey('leave_types.id'), nullable=False)
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    leave_types = relationship('LeaveType', back_populates='leave_sub_types', lazy='joined')
    leaves = relationship('Leave', back_populates='leave_sub_types')

class LeaveType(Base):
    __tablename__ = 'leave_types'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    title = Column(String(255), nullable=False)
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    leaves = relationship('Leave', back_populates='leave_types')
    leave_sub_types = relationship('LeaveSubType', back_populates='leave_types')

class MissedTime(Base):
    __tablename__ = 'missed_times'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    employee_id = Column(String(36), ForeignKey('employees.id'), nullable=False)
    approved_by = Column(String(36), ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    time_log = Column(Time, nullable=False)
    time_log_type = Column(String(255), nullable=False)
    proof = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False, server_default=Text("'Pending'"))
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    employees = relationship('Employee', back_populates='missed_times', lazy='joined')
    users = relationship('User', back_populates='missed_times', lazy='joined')

class ShiftChange(Base):
    __tablename__ = 'shift_changes'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    employee_id = Column(String(36), ForeignKey('employees.id'), nullable=True)
    employee_type_id = Column(String(36), nullable=True)
    user_id = Column(String(36), nullable=True)
    shift_type_id = Column(String(36), ForeignKey('shift_types.id'), nullable=True)
    monday = Column(String(255), nullable=True)
    tuesday = Column(String(255), nullable=True)
    wednesday = Column(String(255), nullable=True)
    thursday = Column(String(255), nullable=True)
    friday = Column(String(255), nullable=True)
    saturday = Column(String(255), nullable=True)
    sunday = Column(String(255), nullable=True)
    status = Column(String(255), nullable=False, server_default=Text("'Pending'"))
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))


    employees = relationship('Employee', back_populates='shift_changes', lazy='joined')
    shift_types = relationship('ShiftType', back_populates='shift_changes', lazy='joined')

class ShiftType(Base):
    __tablename__ = 'shift_types'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    title = Column(String(255), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    employees = relationship('Employee', back_populates='shift_types')
    shift_changes = relationship('ShiftChange', back_populates='shift_types')

class TimeIn(Base):
    __tablename__ = 'time_ins'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    time_log = Column(Time, nullable=False)
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    employees = relationship('Employee', back_populates='time_ins', lazy='joined')
    attendances = relationship('Attendance', back_populates='time_ins')

class TimeOut(Base):
    __tablename__ = 'time_outs'

    id = Column(String(36), primary_key=True, default=Text('UUID()'))
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    time_log = Column(Time, nullable=False)
    active_status = Column(String(255), nullable=False, server_default=Text("'Active'"))
    created_at = Column(DateTime, server_default=Text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=Text('NOW()'))

    employees = relationship('Employee', back_populates='time_outs', lazy='joined')
    attendances = relationship('Attendance', back_populates='time_outs')
#*------end of human resource------

#* LOGISTICS
#? ASSET MANAGEMENT
class Asset(Base):
    __tablename__ = 'assets'

    asset_id = Column(String(60), primary_key=True, default=Text('UUID()'))
    asset_provider_id = Column(String(60), ForeignKey('asset_providers.asset_provider_id'), nullable=True)
    asset_type_id = Column(String(60), ForeignKey('asset_types.asset_type_id'), nullable=True)
    asset_number = Column(Integer, nullable=True)
    asset_cost = Column(Numeric, nullable=True)
    asset_title = Column(String(255), nullable=True)
    asset_description = Column(Text, nullable=True)
    asset_brand = Column(String(255), nullable=True)
    asset_model = Column(String(255), nullable=True)
    asset_serial = Column(String(255), nullable=True)
    asset_acquisition = Column(String(255), nullable=True)
    acquisition_date = Column(DateTime, nullable=True)
    asset_status = Column(String(255), nullable=True, default=('Available'))
    asset_remarks = Column(String(255), nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))
    created_by = Column(String(60), ForeignKey('users.user_id'))

    asset_provider = relationship('Asset_provider', back_populates='asset', lazy='joined')
    asset_type = relationship('Asset_Type', back_populates='asset', lazy='joined')
    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Asset_provider(Base):
    __tablename__ = 'asset_providers'

    asset_provider_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_provider_name = Column(String(255), nullable=True)
    asset_provider_contact = Column(String(255), nullable=True)
    asset_provider_email = Column(String(255), nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    asset = relationship('Asset')

class Asset_Type(Base):
    __tablename__ = 'asset_types'

    asset_type_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_type_title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    asset = relationship('Asset')

class Asset_Warranty(Base):
    __tablename__ = 'asset_warranty'

    warranty_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    warranty_length = Column(Numeric, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    warranty_contact = Column(String(255), nullable=True)
    warranty_email = Column(String(255), nullable=True)
    warranty_note = Column(String(255), nullable=True)
    active_status = Column(Text, nullable=True, default=('Active'))

    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))
    created_by = Column(String(36), ForeignKey('users.user_id'), nullable=True)

    asset_type = relationship('Asset', foreign_keys=[asset_id], lazy='joined')
    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Broken_Asset(Base):
    __tablename__ = 'broken_assets'

    broken_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    remarks = Column(Text, nullable=True)
    broken_date = Column(DateTime, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    created_by = Column(String(60), ForeignKey('users.user_id'))


    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Asset_check_in(Base):
    __tablename__ = 'asset_check_in'

    check_in_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    check_out_id = Column(String(60), ForeignKey('asset_check_out.check_out_id'), nullable=True)
    return_date = Column(DateTime, nullable=True)
    return_location = Column(String(255), nullable=True)
    remarks = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))
    
    check_out_details = relationship('Asset_check_out', foreign_keys=[check_out_id], lazy='joined')

class Asset_check_out(Base):
    __tablename__ = 'asset_check_out'

    check_out_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_id = Column(String(60), ForeignKey('assets.asset_id'), nullable=True)
    user_id = Column(String(60), ForeignKey('users.user_id'), nullable=True)
    department_id = Column(String(60), ForeignKey('department.department_id'), nullable=True)
    location = Column(String(255), nullable=True)
    check_out_date = Column(DateTime, nullable=True)
    check_out_due = Column(DateTime, nullable=True)
    remarks = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))
   
    on_department = relationship('Department', foreign_keys=[department_id], lazy='joined')
    on_user = relationship('User', foreign_keys=[user_id], lazy='joined')
    the_asset = relationship('Asset', foreign_keys=[asset_id], lazy='joined')

#* para saang department (asset? staff? patient? doctor?)
class Department(Base):
    __tablename__ = 'department'

    department_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    department_name = Column(String(255), nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))

class Dispose_Asset(Base):
    __tablename__ = 'dispose_assets'

    dispose_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    remarks = Column(Text, nullable=True)
    dispose_to = Column(String(255), nullable=True)
    dispose_date = Column(DateTime, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    created_by = Column(String(60), ForeignKey('users.user_id'))


    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Events(Base):
    __tablename__ = 'events'

    event_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    event_title = Column(String(255), nullable=True)
    event_message = Column(String(255), nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

class Maintenance(Base):
    __tablename__ = 'maintenances'

    maintenance_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    maintenance_provider_id = Column(String(36), ForeignKey('maintenance_providers.maintenance_provider_id'), nullable=False)
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=False)
    maintenance_name = Column(String(255), nullable=True)
    maintenance_details = Column(String(255), nullable=True)
    maintenance_cost = Column(Numeric, nullable=True)
    maintenance_day = Column(Integer, nullable=True)
    maintenance_due = Column(DateTime, nullable=True)
    maintenance_completed = Column(DateTime, nullable=True)
    maintenance_repeatable = Column(String(255), nullable=True)
    maintenance_status = Column(String(255), nullable=True)
    remarks = Column(String(255), nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    Maintenance_provider = relationship('Maintenance_provider', back_populates='maintenance', lazy='joined')

class Maintenance_provider(Base):
    __tablename__ = 'maintenance_providers'

    maintenance_provider_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    maintenance_provider_name = Column(String(255), nullable=True)
    maintenance_provider_contact = Column(String(255), nullable=True)
    maintenance_provider_email = Column(String(255), nullable=True) 
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    maintenance = relationship('Maintenance')

class Maintenance_Report(Base):
    __tablename__ = 'maintenance_reports'

    maintenance_report_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    maintenance_id = Column(String(36), ForeignKey('maintenances.maintenance_id'), nullable=False)
    maintenance_cost = Column(Numeric, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    maintenance_details = relationship('Maintenance', foreign_keys=[maintenance_id], lazy='joined')

class Missing_Asset(Base):
    __tablename__ = 'missing_assets'

    missing_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    remarks = Column(Text, nullable=True)
    missing_date = Column(DateTime, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    created_by = Column(String(60), ForeignKey('users.user_id'))


    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Repair_Asset(Base):
    __tablename__ = 'repair_assets'

    repair_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    assigned_to = Column(String(255), nullable=True)
    repair_date = Column(DateTime, nullable=True)
    repair_price = Column(Numeric, nullable=True)
    remarks = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    created_by = Column(String(60), ForeignKey('users.user_id'))


    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Request_Asset(Base):
    __tablename__ = 'request_assets'

    request_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_type_id = Column(String(36), ForeignKey('asset_types.asset_type_id'), nullable=True)
    request_brand = Column(String(255), nullable=True)
    request_model = Column(DateTime, nullable=True)
    request_description = Column(Text, nullable=True)
    request_status = Column(String(255), nullable=True)
    request_remark = Column(Text, nullable=True)
    active_status = Column(Text, nullable=True, default=('Active'))

    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))
    created_by = Column(String(36), ForeignKey('users.user_id'), nullable=True)
    updated_by = Column(String(36), ForeignKey('users.user_id'), nullable=True)

    asset_type = relationship('Asset_Type', lazy='joined')
    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')
    updated_by_details = relationship('User', foreign_keys=[updated_by], lazy='joined')

class Sell_Asset(Base):
    __tablename__ = 'sell_assets'

    sell_id = Column(String(36), primary_key=True, default=Text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    sell_to = Column(String(255), nullable=True)
    sell_to_contact = Column(String(255), nullable=True)
    sell_to_email = Column(String(255), nullable=True)
    sell_date = Column(DateTime, nullable=True)
    sell_price = Column(Numeric, nullable=True)
    remarks = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=Text('NOW()'))
    updated_at = Column(DateTime, onupdate=Text('NOW()'))

    created_by = Column(String(60), ForeignKey('users.user_id'))


    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

#? PROCUREMENT MANAGEMENT
#* Blacklist ng ano? may visit_blacklist sa vms
class Blacklist(Base):
    __tablename__ = "blacklist"
    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    # relation with vendor
    vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=True)
    vendor = relationship("Vendor", back_populates="blacklist")
    vendor_name = Column(String(255), nullable=False,index=True)
    email = Column(String(255), nullable=False,index=True)

    remarks = Column(Text, nullable=False,index=True)
    status = Column(String(255), nullable=False,index=True,default="Active")
    
    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class BudgetPlan(Base):
    __tablename__ = "budget_plan"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    given_budget = Column(Float, nullable=False, index=True)
    # remaining_budget = Column(Float, nullable=False, index=True)
    total_spent = Column(Float, nullable=False, index=True,default=0)

    year = Column(String(255), nullable=False, index=True)
    date_from = Column(Date, nullable=False, index=True)
    date_to = Column(Date, nullable=False, index=True)
    status = Column(String(255), nullable=True, index=True,default="active")

    # relation with deparment
    department_id = Column(String(255), ForeignKey("department.id", onupdate='CASCADE'), nullable=True)
    department = relationship("Department", back_populates="budget_plan")
    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)   
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

class Category(Base):
    __tablename__ = "category"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    category_name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True, index=True)
    status = Column(String(255), nullable=True, index=True,default="active")

    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
    # relation with product
    product = relationship("Product", back_populates="category")

   # relation with vendor items
    vendor_bidding_item = relationship("VendorBiddingItems", back_populates="category")


     # relation with vendor
    vendor = relationship("Vendor", back_populates="category")


    # vendor_category = relationship("VendorCategory", back_populates="category") 

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

#* para saang department (staff? patient? doctor?)
class Department(Base):
    __tablename__ = "department"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    department_name = Column(String(255), nullable=False, index=True)
    department_head = Column(String(255), nullable=False, index=True)
    contact_no = Column(String(255), nullable=False, index=True)
    # status = Column(String(255), nullable=True, index=True,default="active")

    employees = relationship("Employee", back_populates="department")

    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
    # relation with budget plan
    budget_plan = relationship("BudgetPlan", back_populates="department")
    # relation with purchase requisition
    purchase_requisition = relationship("PurchaseRequisition", back_populates="department")
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp()) 

#* used by: Time and Attendance
class EmployeeType(Base):
    __tablename__ = "employee_types"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True, index=True)
  
    status = Column(String(255), nullable=True, index=True,default="Active")
    employees = relationship("Employee", back_populates="employee_types")
    
    # relation with user
    created_at = Column(DateTime, nullable=True,default=func.current_timestamp())
    updated_at = Column(DateTime,nullable=True,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

#* used by: please paki-uniform nalang
class Employee(Base):
    __tablename__ = "employees"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(255), nullable=False, index=True)
    last_name = Column(String(255), nullable=False, index=True)
    middle_name = Column(String(255), nullable=True, index=True)
    birthdate = Column(Date, nullable=False, index=True)
    contact_no = Column(String(255), nullable=False, index=True)
    address = Column(String(255), nullable=False)
    status = Column(String(255), nullable=True, index=True,default="Active")
    users = relationship("User", back_populates="employees")
   
     # relation with department
    department_id = Column(String(255), ForeignKey("department.id", onupdate='CASCADE'), nullable=True)
    department = relationship("Department", back_populates="employees")

    employee_type_id = Column(String(255), ForeignKey("employee_types.id", onupdate='CASCADE'), nullable=True)
    employee_types = relationship("EmployeeType", back_populates="employees")



    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

#* para saang invoice? 
class Invoice(Base):
    __tablename__ = "invoice"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)

    prepared_by = Column(String(255), nullable=True, index=True)

    message = Column(Text, nullable=True, index=True)
    
    status = Column(String(255), nullable=True, index=True,default="Pending")
    invoice_date = Column(Date, nullable=False, index=True)
    due_date = Column(Date, nullable=False, index=True)
    billing_address = Column(String(255), nullable=False, index=True)
    amount_paid = Column(String(255), nullable=True, index=True,default=0)
    

    # relation with vendor
    purchase_order_id = Column(String(255), ForeignKey("purchase_order.id", onupdate='CASCADE'),unique=True, nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="invoice")

    # relation with vendor
    created_by = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("Vendor",foreign_keys=[created_by])
    updater = relationship("Vendor",foreign_keys=[updated_by])


    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

#* para saang notification
class Notification(Base):
    __tablename__ = "notification"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=False)
    notif_to = Column(String(255), nullable=False, index=True)

    description = Column(String(255), nullable=True, index=True)
    status = Column(String(20), nullable=False, index=False)

  
    # relation with vendor
    vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=True)
    vendor = relationship("Vendor", back_populates="notification")

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class PaymentMethod(Base):
    __tablename__ = "payment_method"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    method_name = Column(String(255), nullable=False, index=False)
    description = Column(String(255), nullable=True, index=True)

    status = Column(String(20), nullable=False, index=False,default="Active")

    purchase_order = relationship("PurchaseOrder", back_populates="payment_method")

  
    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class PaymentTerms(Base):
    __tablename__ = "payment_terms"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    method_name = Column(String(255), nullable=False, index=False)
  

    description = Column(String(255), nullable=True, index=True)
    status = Column(String(20), nullable=False, index=False,default="Active")

    purchase_order = relationship("PurchaseOrder", back_populates="payment_terms")


      # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class Product(Base):
    __tablename__ = "product"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    # product_pic = Column(String(255), nullable=True, index=True)
    product_name = Column(String(255), nullable=False, index=True)
    estimated_price = Column(DECIMAL, nullable=False, index=True)

    description = Column(Text, nullable=False, index=True)
    estimated_price = Column(Float, nullable=True, index=True)

    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    status = Column(String(255), nullable=True, index=True,default="active")
    # relation with category
    category_id = Column(String(255), ForeignKey("category.id", onupdate='CASCADE'), nullable=True)
    category = relationship("Category", back_populates="product")
    # relation with purchase requisition detail
    purchase_requisition_detail = relationship("PurchaseRequisitionDetail", back_populates="product")
    # relation with user
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class ProjectRequest(Base):
    __tablename__ = "project_request"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    name = Column(Integer, nullable=True, index=True)
    background = Column(Text, nullable=True, index=True)
    coverage = Column(Text, nullable=True, index=True)
    type = Column(String(255), nullable=True, index=True)


    target_beneficiaries = Column(String(255), nullable=True, index=True)
    objectives = Column(String(255), nullable=True, index=True)
    expected_output = Column(Text, nullable=True, index=True)
    assumptions = Column(String(255), nullable=True, index=True)
    constraints = Column(String(255), nullable=True, index=True)
    cost = Column(Float, nullable=True, index=True)
    start_date = Column(Date, nullable=True, index=True)
    end_date = Column(Date, nullable=True, index=True)

    terms_of_reference = relationship("TermsOfReference", back_populates="project_request")

  
   
   
   
    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp()) 

class PurchaseOrderDetail(Base):
    __tablename__ = "purchase_order_detail"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    product_name = Column(String(255), nullable=True, index=True)#unique=True,
    quantity = Column(Integer, nullable=True, index=True)
    category = Column(String(255), nullable=True, index=True)
    product_price = Column(Float, nullable=True, index=True)
    status = Column(String(255), nullable=True, index=True,default="active")
    
    # relation with purchase order
    purchase_order_id = Column(String(255), ForeignKey("purchase_order.id", onupdate='CASCADE'), nullable=True)
    purchase_order = relationship("PurchaseOrder", back_populates="purchase_order_detail")

    return_details = relationship("ReturnDetail", back_populates="purchase_order_detail")


    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
   
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class PurchaseOrder(Base):
    __tablename__ = "purchase_order"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    purchase_order_number = Column(Integer, unique=True, index=True)

    order_date = Column(Date, nullable=True, index=True)
    expected_delivery_date = Column(Date, nullable=True, index=True)
    
    notes = Column(String(255), nullable=True, index=True)
    status = Column(String(255), nullable=True, index=True,default="active")


    subtotal = Column(Float, nullable=False, index=True)
    discount = Column(Float, nullable=False, index=True)
    tax = Column(Float, nullable=False, index=True)
    total_amount = Column(Float, nullable=False, index=True)

    
    # is_rated = Column(Boolean, nullable=True, index=True,default=False)
    shipping_method = Column(String(255), nullable=True, index=True)

    # relation with notif
    # notification = relationship("Notification", back_populates="purchase_order")

    # relation with vendor performance evaluation
    vendor_performance_evaluation = relationship("VendorPerformanceEvaluation", back_populates="purchase_order")

    payment_terms = relationship("PaymentTerms", back_populates="purchase_order")
    payment_terms_id = Column(String(255), ForeignKey("payment_terms.id", onupdate='CASCADE'), nullable=True)

    payment_method = relationship("PaymentMethod", back_populates="purchase_order")

    payment_method_id = Column(String(255), ForeignKey("payment_method.id", onupdate='CASCADE'), nullable=True)

    invoice = relationship("Invoice", back_populates="purchase_order")


     # relation with vendor
    vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=True)
    vendor = relationship("Vendor", back_populates="purchase_order")

    # relation with vendor proposals
    vendor_proposal_id = Column(String(255), ForeignKey("vendor_proposal.id", onupdate='CASCADE'),unique=True, nullable=False)
    vendor_proposal = relationship("VendorProposals", back_populates="purchase_order")

    # relation with purchase order detail
    purchase_order_detail = relationship("PurchaseOrderDetail", back_populates="purchase_order")
    #relation with user 
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class PurchaseRequisitionDetail(Base):
    __tablename__ = "purchase_requisition_detail"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    quantity = Column(Integer, nullable=True, index=True)
    description = Column(Text, nullable=True, index=True)

    new_category = Column(String(255), nullable=True, index=True)
    new_product_name = Column(String(255), nullable=True, index=True)
    estimated_price = Column(Float, nullable=True, index=True)

    # relation with product
    product_id = Column(String(255), ForeignKey("product.id", onupdate='CASCADE'), nullable=True)
    product = relationship("Product", back_populates="purchase_requisition_detail")
    # relation with purchase requisition
    purchase_requisition_id = Column(String(255), ForeignKey("purchase_requisition.id", onupdate='CASCADE',ondelete='CASCADE'), nullable=False)
    purchase_requisition = relationship("PurchaseRequisition", back_populates="purchase_requisition_detail")
    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])

    status = Column(String(255), nullable=True, index=True,default="active")
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp()) 

class PurchaseRequisition(Base):
    __tablename__ = "purchase_requisition"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    purchase_requisition_number = Column(Integer, unique=True, index=True)
    purpose = Column(String(255), nullable=False, index=True)

    message = Column(Text, nullable=False, index=True)
    status = Column(String(255), nullable=False, index=True)
    date_approved = Column(DateTime, nullable=True, index=True)


    
    # if approved
    approved_by = Column(String(255), nullable=True, index=True)
    given_budget = Column(Float, nullable=True, index=True)
    estimated_amount = Column(Float, nullable=True, index=True,default=0)
    has_quotation = Column(Boolean, nullable=True, default=False)#remvee

        # relation with notif
    # notification = relationship("Notification", back_populates="purchase_requisition")


    # if rejected
    reason = Column(String(255), nullable=True, index=True)
    # relation with department
    department_id = Column(String(255), ForeignKey("department.id", onupdate='CASCADE'), nullable=False)
    department = relationship("Department", back_populates="purchase_requisition")
    # relation with purchase requisition detail
    purchase_requisition_detail = relationship("PurchaseRequisitionDetail", back_populates="purchase_requisition")
    # relation with request quotation
    request_quotation = relationship("RequestQuotation", back_populates="purchase_requisition")
    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class RelatedDocuments(Base):
    __tablename__ = "related_documents"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    attachment = Column(String(255), index=True)

    request_quotation_id = Column(String(255), ForeignKey("request_quotation.id", onupdate='CASCADE'), nullable=True)
    
    request_quotation = relationship("RequestQuotation", back_populates="related_documents")


  
    # relation with vendor proposals
    vendor_proposal_id = Column(String(255), ForeignKey("vendor_proposal.id", onupdate='CASCADE'), nullable=True)
    vendor_proposal = relationship("VendorProposals", back_populates="related_documents")

    status = Column(String(255), nullable=True, index=True,default="active")
 
     
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class RequestQuotation(Base):
    __tablename__ = "request_quotation"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    request_quotation_number = Column(Integer, unique=True, index=True)
    
    message = Column(Text, nullable=True, index=True)
    status = Column(String(255), nullable=True, index=True)
    # active_status = Column(String(255), nullable=True, index=True,default="Active")

    due_date = Column(DateTime, nullable=False, index=True)
    prepared_by = Column(String(255), nullable=False, index=True)
    # has_proposal = Column(Boolean, nullable=False, index=True,default=False)
    quotation_code = Column(String(255), nullable=False, index=True)
    rfq_type = Column(String(255), nullable=False, index=True)

    # approver_name = Column(String(255), nullable=True, index=True)
    # approval_date = Column(Date, nullable=True, index=True)
    # reject_reason = Column(Text, nullable=True, index=True)

    
    # relation with related documents

    # vendor_id = Column(ForeignKey("vendor.id"), primary_key=True)

    # vendor = relationship("Vendor", back_populates="request_quotation")

    
    related_documents = relationship("RelatedDocuments", back_populates="request_quotation")

    # request_quotation_vendor = relationship("RequestQuotationVendor", back_populates="request_quotation")

    request_quotation_vendor = relationship("RequestQuotationVendor",foreign_keys='[RequestQuotationVendor.request_quotation_id]')
    
    # relation with purhcase requisition
    purchase_requisition_id = Column(String(255), ForeignKey("purchase_requisition.id", onupdate='CASCADE'), nullable=True)
    # purchase_requisition_id = Column(ForeignKey("purchase_requisition.id"), primary_key=True)

    purchase_requisition = relationship("PurchaseRequisition", back_populates="request_quotation")
    # relation with vendor
    # vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=True)

 
    # relation with terms of reference
    terms_of_reference_id = Column(String(255), ForeignKey("terms_of_reference.id", onupdate='CASCADE'), nullable=True)
    terms_of_reference = relationship("TermsOfReference", back_populates="request_quotation")

    # relation with vendor proposals
    vendor_proposal = relationship("VendorProposals", back_populates="request_quotation")

    

    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class ReturnDetail(Base):
    __tablename__ = "return_details"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    quantity = Column(Integer, nullable=False)
    status = Column(String(255), nullable=True, index=True,default="Active")

    # relation with user type
    purchase_order_detail_id = Column(String(255), ForeignKey("purchase_order_detail.id"), nullable=True)
    purchase_order_detail = relationship("PurchaseOrderDetail", back_populates="return_details")
  

    return_id = Column(String(255), ForeignKey("returns.id"), nullable=True)
    returns = relationship("Return", back_populates="return_details")
    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class Return(Base):
    __tablename__ = "returns"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    return_date = Column(Date, nullable=False)
    return_status = Column(String(255), nullable=True, index=True)
    return_type = Column(String(255), nullable=True, index=True)

    return_details = relationship("ReturnDetail", back_populates="returns")




  
  # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])

    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class RequestQuotationVendor(Base):
    __tablename__ = "request_quotation_vendor"

        
    # relation with related
    vendor_id = Column(ForeignKey("vendor.id"), primary_key=True)
    rfq_pr_id = Column(String(255),ForeignKey("request_quotation.purchase_requisition_id"), nullable=True)
    rfq_status = Column(String(255), nullable=True, index=True,default="Pending")
    approver_name = Column(String(255), nullable=True, index=True)
    approval_date = Column(Date, nullable=True, index=True)
    reject_reason = Column(Text, nullable=True, index=True)


    vendor = relationship("Vendor", back_populates="request_quotation_vendor")

    request_quotation_id = Column(ForeignKey("request_quotation.id"), primary_key=True)
    rfq_tor_id = Column(String(255),ForeignKey("request_quotation.terms_of_reference_id"), nullable=True)


    # request_quotation = relationship("RequestQuotation",foreign_keys=[request_quotation_id])
    # rfq_pr = relationship("RequestQuotation",foreign_keys=[rfq_pr_id])
    # rfq_tor = relationship("RequestQuotation",foreign_keys=[rfq_tor_id])

 
    sa.UniqueConstraint(vendor_id, rfq_pr_id) 
    


    # relation with notif
    # notification = relationship("Notification", back_populates="request_quotation")

    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
    # relation with vendor proposals
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class TermsOfReference(Base):
    __tablename__ = "terms_of_reference"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    title =Column(String(255), nullable=True, index=True)
    background = Column(Text, nullable=True, index=True)
    objective = Column(Text, nullable=True, index=True)
    scope_of_service = Column(Text, nullable=True, index=True)
    tor_deliverables = Column(Text, nullable=True, index=True)
    qualifications = Column(Text, nullable=True, index=True)
    reporting_and_working_arrangements = Column(Text, nullable=True, index=True)
    tor_annex_technical_specifications = Column(Text, nullable=True, index=True)
    tor_annex_key_experts = Column(Text, nullable=True, index=True)
    tor_annex_deliverables = Column(Text, nullable=True, index=True)
    tor_annex_terms_conditions = Column(Text, nullable=True, index=True)
    status = Column(String(255), nullable=True, index=True)

    # approver_name = Column(String(255), nullable=True, index=True)
    # approval_date = Column(Date, nullable=True, index=True)
    # reject_reason = Column(String(255), nullable=True, index=True)

    #   relation with project request
    project_id = Column(String(255), ForeignKey("project_request.id"), nullable=True)

    project_request = relationship("ProjectRequest", back_populates="terms_of_reference")
   
    # relation with request quotation
    request_quotation = relationship("RequestQuotation", back_populates="terms_of_reference")


    # relation with vendor
    vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=True)
    vendor = relationship("Vendor", back_populates="terms_of_reference")

    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
   
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class Utilities(Base):
    __tablename__ = "utilities"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    utility_type = Column(String(255), nullable=True, index=True)
    attachment = Column(String(255), nullable=True, index=True)
    utility_amount = Column(String(255), nullable=True, index=True)
    due_date = Column(String(255), nullable=True, index=True)
    notes = Column(Text, nullable=True, index=True)

  


    # relation with vendor
    vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=True)
    vendor = relationship("Vendor", back_populates="utilities")

    status = Column(String(255), nullable=True, index=True,default="pending")

    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])

    # relation with purchase order


    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class VendorAuditTrail(Base):
    __tablename__ = "vendor_audit_trail"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    crud = Column(String(255), nullable=False, index=True)
    client_ip = Column(String(255), nullable=True, index=True)
    table = Column(String(255), nullable=False, index=True)
    payload = Column(Text, nullable=True, index=True)

    # relation with vendor
    vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=False)
    vendor = relationship("Vendor", back_populates="vendor_audit_trail")
    created_at = Column(DateTime, default=func.current_timestamp())

class VendorBiddingItems(Base):
    __tablename__ = "vendor_bidding_item"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    # relation with category
    category_id = Column(String(255), ForeignKey("category.id", onupdate='CASCADE'), nullable=True)
    category = relationship("Category", back_populates="vendor_bidding_item") 
    product_name = Column(String(255), nullable=True, index=True)#unique
    description = Column(Text, nullable=True, index=True)
    quantity = Column(Integer, nullable=True, index=True)
    price_per_unit = Column(Float, nullable=True, index=True)
    status = Column(String(255), nullable=True, index=True,default="active")


    
    # relation with vendor proposal
    vendor_proposal_id = Column(String(255), ForeignKey("vendor_proposal.id", onupdate='CASCADE'), nullable=True)
    vendor_proposal = relationship("VendorProposals", back_populates="vendor_bidding_item")

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class VendorCategory(Base):
    __tablename__ = "vendor_category"
    
    id = Column(String(255), primary_key=True, default=uuid.uuid4)

    category_id = Column(String(255), ForeignKey("category.id", onupdate='CASCADE'), nullable=False)
    category = relationship("Category", back_populates="vendor_category")


     # relation with vendor
    vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=False)
    vendor = relationship("Vendor", back_populates="vendor_category")

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class VendorPerformanceEvaluation(Base):
    __tablename__ = "vendor_performance_evaluation"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    message = Column(Text, nullable=True, index=True)


    cost = Column(String(255), nullable=True, index=True)
    timeliness = Column(String(255), nullable=True, index=True)
    reliability = Column(String(255), nullable=True, index=True)
    quality = Column(String(255), nullable=True, index=True)
    availability = Column(String(255), nullable=True, index=True)
    reputation = Column(String(255), nullable=True, index=True)




    status = Column(String(255), nullable=True, index=True,default="active")

    # relation with user
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])
    # relation with vendor
    # vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=True)
    # vendor = relationship("Vendor", back_populates="vendor_performance_evaluation")

    # relation with purchase order
        
    # relation with vendor
    purchase_order_id = Column(String(255), ForeignKey("purchase_order.id", onupdate='CASCADE'),unique=True, nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="vendor_performance_evaluation")

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

class VendorProposals(Base):
    __tablename__ = "vendor_proposal"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    proposal_number = Column(Integer, unique=True, index=True)

    subtotal = Column(Float, nullable=True, index=True)
    discount = Column(Float, nullable=True, index=True)
    tax = Column(Float, nullable=True, index=True)
    total_amount = Column(String(255), nullable=True, index=True)
    prepared_by = Column(String(255), nullable=True, index=True)
    contact_no = Column(String(255), nullable=True, index=True)

    message = Column(Text, nullable=True, index=True)
    notes = Column(Text, nullable=True, index=True)
    
    status = Column(String(255), nullable=True, index=True)
    # delivery_days = Column(String(255), nullable=True, index=True)
    arrival_date = Column(Date, nullable=True, index=True)
    
    is_ordered = Column(Boolean, nullable=True, index=True,default=False)


    # relation with vendor bidding items
    vendor_bidding_item = relationship("VendorBiddingItems", back_populates="vendor_proposal")
     # relation with vendor purchase order
    purchase_order = relationship("PurchaseOrder", back_populates="vendor_proposal")

    # relation with related documents
    related_documents = relationship("RelatedDocuments", back_populates="vendor_proposal")


    # relation with request quotation
    request_quotation_id = Column(String(255), ForeignKey("request_quotation.id", onupdate='CASCADE'), nullable=False)
    # rfq_pr_id = Column(String(255), ForeignKey("request_quotation.purchase_requisition_id"),unique=True, nullable=False)
    # rfq_vendor_id = Column(String(255), ForeignKey("request_quotation.vendor_id"),unique=True, nullable=False)

    request_quotation = relationship("RequestQuotation", back_populates="vendor_proposal")
    # relation with vendor
    created_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    updated_by = Column(String(255), ForeignKey("users.id", onupdate='CASCADE'), nullable=True)
    creator = relationship("User",foreign_keys=[created_by])
    updater = relationship("User",foreign_keys=[updated_by])

    awarded_by = Column(String(255), nullable=True, index=True)

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())


    sa.UniqueConstraint(created_by, request_quotation_id) 

class VendorTimeLog(Base):
    __tablename__ = "vendor_time_log"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    logged_date = Column(DateTime, nullable=False, index=True)
    logged_type = Column(String(255), nullable=False, index=True)
    client_ip = Column(String(255), nullable=True, index=True)

    # relation with vendor
    vendor_id = Column(String(255), ForeignKey("vendor.id", onupdate='CASCADE'), nullable=False)
    vendor = relationship("Vendor", back_populates="vendor_time_log")

class Vendor(Base):
    __tablename__ = "vendor"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)

    vendor_logo = Column(String(255), nullable=False,unique=True,index=True)
    vendor_name = Column(String(255), nullable=False,unique=True,index=True)

    contact_person = Column(String(255), nullable=True, index=True)
    contact_no = Column(String(255), nullable=True, index=True)
    vendor_website = Column(String(255), nullable=True, index=True)
    email = Column(String(255), nullable=False,unique=True,index=True)
    organization_type = Column(String(255), nullable=True, index=True)

    region = Column(String(255), nullable=False, index=True)
    province = Column(String(255), nullable=False, index=True)
    municipality = Column(String(255), nullable=False, index=True)
    barangay = Column(String(255), nullable=False, index=True)

    street = Column(String(255), nullable=True, index=True)
    # relation with category
    category_id = Column(String(255), ForeignKey("category.id", onupdate='CASCADE'), nullable=True)#created by

    category = relationship("Category", back_populates="vendor") 

    # vendor_category = relationship("VendorCategory", back_populates="vendor") 
    # relationship with audit trail
    vendor_audit_trail = relationship("VendorAuditTrail", back_populates="vendor")
    # relationship with time log
    vendor_time_log = relationship("VendorTimeLog", back_populates="vendor")
    
    status = Column(String(255), nullable=True, index=True,default="active")

    
  # relation with user
    # created_by = Column(String(255), ForeignKey("users.id"), nullable=True)
    # updated_by = Column(String(255), ForeignKey("users.id"), nullable=True)
    # creator = relationship("User",foreign_keys=[created_by])
    # updater = relationship("User",foreign_keys=[updated_by])

    users = relationship("User", back_populates="vendor")

  
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())

    # password = Column(String(255), nullable=False)

    # relation with request quotation
    # request_quotation = relationship("RequestQuotation", back_populates="vendor")

    # relation with terms of reference
    terms_of_reference = relationship("TermsOfReference", back_populates="vendor")

    # relation wtih utilities
    utilities = relationship("Utilities", back_populates="vendor")


    
    # relation with vendor
    purchase_order = relationship("PurchaseOrder", back_populates="vendor")

    # relation with notif
    notification = relationship("Notification", back_populates="vendor")


    request_quotation_vendor = relationship("RequestQuotationVendor", back_populates="vendor")

    # relation with vendor evaluation results
    # vendor_performance_evaluation = relationship("VendorPerformanceEvaluation", back_populates="vendor")

    # relation with blacklist

    blacklist = relationship("Blacklist", back_populates="vendor")

  
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime,
                    default=func.current_timestamp(),
                    onupdate=func.current_timestamp())












