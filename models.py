import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy import Text, String, Boolean, Date, DateTime, Numeric, Integer, Time, Float, DECIMAL, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

#! YUNG USER TABLE (AND PROFILES/ROLES) WAG MUNA DITO
#! PAKIAYOS LAHAT NG MAY EMPLOYEE HEHE

#** CORE
#? VISITOR MANAGEMENT
class Station(Base):
    __tablename__ = 'stations'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)

    appointment = relationship('Appointment', back_populates='station')

class Health_Form(Base):
    __tablename__ = 'health_forms'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    symptoms = Column(String(255), nullable=True)
    condition = Column(String(255), nullable=False)
    date_submitted = Column(Date, nullable=False, default=text('NOW()'))

    user = relationship('User', back_populates='health_form')
    health_pass = relationship('Pass', back_populates='health_form')

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
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

    id = Column(String(36), primary_key=True, default=text('UUID()'))
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

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    pass_id = Column(String(36), ForeignKey('passes.id'), nullable=True)
    image = Column(String(255), nullable=False)
    remarks = Column(Text, nullable=False)
    check_in = Column(DateTime, default=text('NOW()'))
    check_out = Column(DateTime, nullable=True)

    visit_pass = relationship('Pass', back_populates='visit')
    appointment = relationship('Appointment', secondary='join(Pass, Appointment, Pass.appointment_id == Appointment.id)', secondaryjoin='Appointment.id == Pass.appointment_id', uselist=False, viewonly=True)
    health_form = relationship('Health_Form', secondary='join(Pass, Health_Form, Pass.health_form_id == Health_Form.id)', secondaryjoin='Health_Form.id == Pass.health_form_id', uselist=False, viewonly=True)
    user = relationship('User', secondary='join(Pass, User, Pass.user_id == User.id)', secondaryjoin='User.id == Pass.user_id', uselist=False, viewonly=True)

class Visit_Blacklist(Base):
    __tablename__ = 'blacklists'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    image = Column(String(255), nullable=True)
    remarks = Column(Text, nullable=False)
    is_active = Column(Boolean, default=text('1'))
    is_seen = Column(Boolean, default=text('0'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    user = relationship('User', back_populates='blacklist', uselist=False)
    profile = relationship('User_Profile', secondary='join(User, User_Profile, User.id == User_Profile.user_id)', secondaryjoin='User_Profile.user_id == User.id', viewonly=True, uselist=False)

#? TREATMENT MANAGEMENT
class InPatient(Base):
    __tablename__ = "inpatients"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    surgeries = relationship('Surgery', back_populates='inpatient')
    treatments = relationship('Treatment', back_populates='inpatient')
    lab_requests = relationship('LabRequest', back_populates='inpatient')

class LabRequest(Base):
    __tablename__ = "lab_requests"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    lab_test_id = Column(String(36), ForeignKey("lab_tests.id"))
    # lab_result_id = Column(String(36), ForeignKey("lab_results.id"))
    inpatient_id = Column(String(36), ForeignKey("inpatients.id"))
    outpatient_id = Column(String(36), ForeignKey("outpatients.id"))
    quantity = Column(Numeric(15,2), nullable=False)

    lab_request_no = Column(String(100))

    is_active = Column(String(100), default='ACTIVE')
    status = Column(String(100), default='PENDING')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    lab_result = relationship('LabResult', back_populates='lab_request')
    lab_test = relationship('LabTest', back_populates='lab_requests')

    inpatient = relationship('InPatient', back_populates='lab_requests')
    outpatient = relationship('OutPatient', back_populates='lab_requests')

#* used by: MRS
class LabResult(Base):
    __tablename__ = "lab_results"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    lab_request = relationship('LabRequest', back_populates='lab_result')

class LabTest(Base):
    __tablename__ = "lab_tests"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    name = Column(String(100), unique=True)
    description = Column(Text)
    fee = Column(Numeric(15,2))

    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    lab_requests = relationship('LabRequest', back_populates='lab_test')

class OutPatient(Base):
    __tablename__ = "outpatients"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    treatments = relationship('Treatment', back_populates='outpatient')
    lab_requests = relationship('LabRequest', back_populates='outpatient')

class SurgeryInCharge(Base):
    __tablename__ = "surgery_in_charge"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    professional_fee = Column(Numeric(15,2))


    in_charge_id = Column(ForeignKey('users.id'))
    surgery_id = Column(ForeignKey('surgeries.id'))

    in_charge = relationship('User', back_populates="handled_surgeries")
    surgery = relationship("Surgery", back_populates="in_charge")

class SurgeryType(Base):
    __tablename__ = "surgery_types"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    name = Column(String(100), unique=True)
    description = Column(Text)
    price = Column(Numeric(15,2))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    surgeries = relationship("Surgery", back_populates="surgery_type")

class Surgery(Base):
    __tablename__ = "surgeries"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    inpatient = relationship('InPatient', back_populates='surgeries')
    surgery_type = relationship("SurgeryType", back_populates="surgeries")

    in_charge = relationship('SurgeryInCharge', back_populates="surgery")

class TreatmentType(Base):
    __tablename__ = "treatment_types"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    name = Column(String(100), unique=True)
    room = Column(String(100))
    description = Column(Text)
    fee = Column(Numeric(15,2))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    treatments = relationship('Treatment', back_populates='treatment_type')

class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    inpatient = relationship('InPatient', back_populates='treatments')
    outpatient = relationship('OutPatient', back_populates='treatments')
    physician = relationship('User', back_populates='treatments')
    treatment_type = relationship('TreatmentType', back_populates='treatments')

#? MEDICAL RECORDS
class Doctor(Base):
    __tablename__ = 'doctors'

    doc_id          = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at      = Column(DateTime, default=text('NOW()'))
    updated_at      = Column(DateTime, onupdate=text('NOW()'))

    diagnosisdocFK        = relationship('Diagnosis', back_populates="docdiagnosisFK")
    progressnoteFK        = relationship('ProgressNote', back_populates="docentryFK")
    doctorprescriptionFK  = relationship('Prescription', back_populates="docprescriptionFK")   

    doctor_profilesFK    = relationship('UserProfile', back_populates='docProfileFK')

class Patient(Base):
    __tablename__ = 'patients'

    patient_id      = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at      = Column(DateTime, default=text('NOW()'))
    updated_at      = Column(DateTime, onupdate=text('NOW()'))

    patientFK             = relationship('Record', back_populates="patientrecordFK")
    patientdischargeFK    = relationship('Discharge', back_populates="dischargeFK")

    patient_profilesFK    = relationship('UserProfile', back_populates='patientProfileFK')
    patientrequestFK      = relationship('Request', back_populates='requesterFK')

    historyrecordFK         = relationship('History', back_populates="historyFK")

class Record(Base):
    __tablename__ = 'patient_records'

    patient_record_id       = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_id              = Column(String(36), ForeignKey('patients.patient_id'))
    # record_id               = Column(String(8), default=base64.b64encode(os.urandom(6)).decode('ascii'))
    # record_id               = Column(String(8), default=text('UUID()'))
    created_at              = Column(DateTime, default=text('NOW()'))
    updated_at              = Column(DateTime, onupdate=text('NOW()'))


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

    history_id              = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at              = Column(DateTime, default=text('NOW()'))
    updated_at              = Column(DateTime, onupdate=text('NOW()'))

    historyFK               = relationship('Patient', back_populates="historyrecordFK")

class Problem(Base):
    __tablename__ = 'problems'

    problem_id              = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_record_id       = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    problem_name            = Column(String(255), nullable=False)
    problem_note            = Column(String(255), nullable=False)
    active_status           = Column(String(255), nullable=False)
    date_occured            = Column(Date, nullable=False)
    date_resolved           = Column(Date, nullable=True)
    created_at              = Column(DateTime, default=text('NOW()'))
    updated_at              = Column(DateTime, onupdate=text('NOW()'))
    
    problemFK               = relationship('Record', back_populates="problemrecordFK")

class Diagnosis(Base):
    __tablename__ = 'diagnosis'

    diagnosis_id      = Column(String(36), primary_key=True, default=text('UUID()'))
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

    lab_result_id       = Column(String(36), primary_key=True, default=text('UUID()'))
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

    prescription_id           = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_record_id         = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    medication_name           = Column(String(255), nullable=True)
    medication_type           = Column(String(255), nullable=True)
    dosage                    = Column(String(255), nullable=True)
    quantity                  = Column(String(255), nullable=False)
    frequency                 = Column(String(255), nullable=True)
    med_taken_for             = Column(String(255), nullable=True)
    doc_id                    = Column(String(36), ForeignKey('doctors.doc_id'))
    prescription_notes        = Column(String(255), nullable=False)
    created_at                = Column(DateTime, default=text('NOW()'))
    updated_at                = Column(DateTime, onupdate=text('NOW()'))
    

    docprescriptionFK       = relationship('Doctor', back_populates="doctorprescriptionFK")    
    #prescriptiondetailsFK   = relationship('PrescriptionDetail', back_populates="prescribeFK")
    prescriptionsFK         = relationship('Record', back_populates="prescriptionrecordFK")

class ProgressNote(Base):
    __tablename__ = 'progress_notes'

    progress_note_id        = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_record_id       = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    # progress_note_id    =  Column(String(36), ForeignKey('progress_notes.progress_note_id'))
    doc_id                  =  Column(String(36), ForeignKey('doctors.doc_id'))
    reason_for_consultation = Column(String(255), nullable=False)
    physical_examination    = Column(String(255), nullable=False)
    impression              = Column(String(255), nullable=False)
    recommendation          = Column(String(255), nullable=False)
    consultation_date        = Column(Date, nullable=True)
    next_appointment        = Column(Date, nullable=True)
    created_at              = Column(DateTime, default=text('NOW()'))
    updated_at              = Column(DateTime, onupdate=text('NOW()'))
    
   # progressdetailFK    = relationship('ProgressNoteDetail', back_populates="progressFK")
    progressnoteFK          = relationship('Record', back_populates="progressnoterecordFK")
    docentryFK              = relationship('Doctor',back_populates="progressnoteFK")

class CallLog(Base):
    __tablename__ = 'patient_call_logs'

    patient_call_log_id     = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_record_id       = Column(String(36), ForeignKey('patient_records.patient_record_id'))

    call_logFK              = relationship('Record', back_populates="call_logrecordFK")
    logsFK                  = relationship('CallLogDetail', back_populates="call_logsFK")

class CallLogDetail(Base):
    __tablename__ = 'patient_call_log_details'

    call_log_detail_id     = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_call_log_id    = Column(String(36), ForeignKey('patient_call_logs.patient_call_log_id'))
    call_log_date          = Column(Date, nullable=False)
    # payor_called           = Column(String(255), nullable=False)
    contact_first_name     = Column(String(255), nullable=False)
    contact_last_name      = Column(String(255), nullable=False)
    contact_phone          = Column(String(255), nullable=False)
    call_details           = Column(String(255), nullable=False)
    follow_up_date         = Column(Date, nullable=True)
    created_at             = Column(DateTime, default=text('NOW()'))
    updated_at             = Column(DateTime, onupdate=text('NOW()'))

    call_logsFK            = relationship('CallLog', back_populates="logsFK")

class Allergy(Base):
    __tablename__ = 'allergies'

    allergy_id             = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_record_id      = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    allergen               = Column(String(255), nullable=True)
    reaction               = Column(String(255), nullable=True)
    severity               = Column(String(255), nullable=True)
    comment                = Column(String(255), nullable=True)
    created_at             = Column(DateTime, default=text('NOW()'))
    updated_at             = Column(DateTime, onupdate=text('NOW()'))

    allergiesFK            = relationship('Record', back_populates="record_allergyFK")

class Immunization(Base):
    __tablename__ = 'immunizations'

    immunization_id        = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_record_id      = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    vaccine                = Column(String(255), nullable=True)
    type                   = Column(String(255), nullable=True)
    date_given             = Column(Date, nullable=True)
    administered_by        = Column(String(255), nullable=True)
    created_at             = Column(DateTime, default=text('NOW()'))
    updated_at             = Column(DateTime, onupdate=text('NOW()'))

    immunizationsFK        = relationship('Record', back_populates="record_immunizationFK")

class Medication(Base):
    __tablename__ = 'medications'

    medication_id          = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at             = Column(DateTime, default=text('NOW()'))
    updated_at             = Column(DateTime, onupdate=text('NOW()'))

    medicationsFK          = relationship('Record', back_populates="record_medicationFK")

class Attachment(Base):
    __tablename__ = 'attachments'

    attachment_id          = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_record_id      = Column(String(36), ForeignKey('patient_records.patient_record_id'))
    attachment             = Column(String(255), nullable=True)
    type                   = Column(String(255), nullable=True)
    created_at             = Column(DateTime, default=text('NOW()'))
    updated_at             = Column(DateTime, onupdate=text('NOW()'))

    attachmentsFK          = relationship('Record', back_populates="record_attachmentFK")

class Request(Base):
    __tablename__ = 'requests'

    request_id              = Column(String(36), primary_key=True, default=text('UUID()'))
    review_by               = Column(String(36), ForeignKey('users.user_id'))
    patient_id              = Column(String(36), ForeignKey('patients.patient_id'))
    request_information     = Column(String(255), nullable=True)
    disclosure_reason       = Column(String(255), nullable=True)
    delivery                = Column(String(255), nullable=True)
    email                   = Column(String(255), nullable=True)
    requested_file          = Column(String(255), nullable=True)
    review_reason           = Column(String(255), nullable=True)
    active_status           = Column(String(255), nullable=False, default="Pending")
    created_at              = Column(DateTime, nullable=True, default=text('NOW()'))
    updated_at              = Column(DateTime, nullable=True, onupdate=text('NOW()'))

    reviewbyFK = relationship('User', back_populates='requestreviewFK')
    requesterFK = relationship('Patient', back_populates='patientrequestFK')

#? PATIENT MANAGEMENT

class DischargeManagement(Base):
    __tablename__ = 'discharge_management'

    discharge_id = Column(String(255), primary_key=True, default=text('UUID()'))
    discharge_no = Column(String(255), nullable=False)
    patient_id = Column(String(255), ForeignKey('patient_registration.patient_id'), nullable=True)
    admission_id = Column(String(255), ForeignKey('inpatients.admission_id'), nullable=True)
    reason_of_admittance = Column(String(255), nullable=False)
    diagnosis_at_admittance = Column(String(255), nullable=False)
    date_admitted = Column(DateTime, default=text('NOW()'))
    treatment_summary = Column(String(255), nullable=False)
    discharge_date = Column(Date, nullable=True)
    physician_approved = Column(String(255), nullable=False)
    discharge_diagnosis = Column(String(255), nullable=False)
    further_treatment_plan = Column(String(255), nullable=False)
    next_check_up_date = Column(Date, nullable=True)
    client_consent_approval = Column(String(255), nullable=False)
    # medication = Column(String(255), nullable=True)
    # dosage = Column(String(255), nullable=True)
    # frequency = Column(String(255), nullable=True)
    # ending_date = Column(Date, nullable=True)
    active_status = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    discharge_managementFk = relationship('PatientRegistration', foreign_keys=[patient_id])
    discharge_inpatientFk = relationship('Inpatient', foreign_keys=[admission_id])

class Discount(Base):
    __tablename__ = 'discount_privillages'

    dp_id = Column(String(36), primary_key=True, default=text('UUID()'))
    ph_id = Column(String(255), nullable=True)
    end_of_validity = Column(String(255), nullable=True)
    sc_id = Column(String(255), nullable=True)
    municipality = Column(String(255), nullable=True)
    pwd_id = Column(String(255), nullable=True)
    type_of_disability = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

class Inpatient(Base):
    __tablename__ = 'inpatients'

    admission_id = Column(String(255), primary_key=True, default=text('UUID()'))
    inpatient_no = Column(String(255), nullable=False)
    patient_id = Column(String(36), ForeignKey('patient_registration.patient_id'), nullable=True)
    room_number = Column(String(36), ForeignKey('rooms.room_id'), nullable=False)
    date_admitted = Column(DateTime, default=text('NOW()'))
    reason_of_admittance = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    diagnosis = Column(String(255), nullable=True)
    tests = Column(String(255), nullable=True)
    treatments = Column(String(255), nullable=True)
    surgery = Column(String(255), nullable=True)
    is_accepting_visits = Column(String(255), nullable=True)
    patient_status = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    room = relationship('Room', foreign_keys=[room_number])
    inpatientsFk = relationship('PatientRegistration', foreign_keys=[patient_id])

class MedicalSupplies_PR(Base):
    __tablename__= 'medicalsupplies_pr'

    medicsupp_prid= Column(String(36), primary_key=True,  default=text('UUID()'))
    ms_no = Column(Integer, nullable=False,unique=True, index=True)
    med_id = Column(String(36), ForeignKey("medicine.med_id"),nullable=True)
    quantity = Column(Integer,nullable=False)
    prescription_id = Column(String(36), ForeignKey("prescriptions.prescription_id"),nullable=True)
    created_at = Column(DateTime,nullable=False, default=text('NOW()'))
    updated_at = Column(DateTime,nullable=True, default=text('NOW()'))

    prescription_info = relationship("Prescription", foreign_keys=[prescription_id])
    med_id_FK = relationship('Medicine', foreign_keys=[med_id])

class MedicalHistory(Base):
    __tablename__ = 'medical_history'

    medical_history_number = Column(String(36), primary_key=True, default=text('UUID()'))
    # patient_id = Column(String(255), ForeignKey('patient_registration.patient_id'), nullable=True)
    # prev_hospital = Column(String(255), nullable=True)
    # prev_doctor = Column(String(255), nullable=True)
    prev_diagnosis = Column(String(255), nullable=True)
    prev_treatments = Column(String(255), nullable=True)
    prev_surgeries = Column(String(255), nullable=True)
    prev_medications = Column(String(255), nullable=True)
    allergies = Column(String(255), nullable=True)
    health_conditions = Column(String(255), nullable=True)
    special_privillages = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

class Medicine_PR(Base):
    __tablename__= 'medicine_pr'

    medpr_id= Column(String(36), primary_key=True, default=text('UUID()'))
    medicine_no = Column(Integer, nullable=False,unique=True, index=True)
    med_id = Column(String(36), ForeignKey("medicine.med_id"),nullable=True)
    quantity = Column(Integer,nullable=False)
    intake = Column(String(255),nullable=False)
    frequency = Column(String(255),nullable=False)
    dosage = Column(String(255),nullable=False)
    doctor_prescribed = Column(String(255),nullable=False)
    prescription_id = Column(String(36), ForeignKey("prescriptions.prescription_id"),nullable=True)
    med_pres_status = Column(String(255),nullable=False, default="Unpaid")
    created_at = Column(DateTime,nullable=False, default=text('NOW()'))
    updated_at = Column(DateTime,nullable=True, default=text('NOW()'))

    med_id_FK = relationship('Medicine', foreign_keys=[med_id])
    prescription_FK = relationship('Prescription', foreign_keys=[prescription_id])

class Outpatient(Base):
    __tablename__ = 'outpatients'

    outpatient_id = Column(String(255), primary_key=True, default=text('UUID()'))
    outpatient_no = Column(String(255), nullable=False)
    patient_id = Column(String(255), ForeignKey('patient_registration.patient_id'), nullable=True)
    walk_in_date = Column(DateTime, default=text('NOW()'))
    purpose = Column(String(255), nullable=False)
    test = Column(String(255), nullable=True)
    treatment_summary = Column(String(255), nullable=True)
    # medication = Column(String(255), nullable=True)
    # dosage = Column(String(255), nullable=True)
    # frequency = Column(String(255), nullable=True)
    # ending_date = Column(Date, nullable=True)
    patient_status = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    patient_registration = relationship('PatientRegistration')

class PatientRegistration(Base):
    __tablename__ = 'patient_registration'

    patient_id = Column(String(36), primary_key=True, default=text('UUID()'))
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    sex = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    weight = Column(String(255), nullable=False)
    height = Column(String(255), nullable=False)
    blood_type = Column(String(255), nullable=False)
    guardian = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    contact_number = Column(String(255), nullable=False)
    hospital_employee = Column(String(255), nullable=False)
    medical_history_number = Column(String(36), ForeignKey('medical_history.medical_history_number'), nullable=True)
    dp_id = Column(String(36), ForeignKey('discount_privillages.dp_id'), nullable=True)
    patient_type = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    medical_history = relationship('MedicalHistory')
    discount_privillages = relationship('Discount')

class Prescription(Base):
    __tablename__= 'prescriptions'

    prescription_id= Column(String(36), primary_key=True,  default=text('UUID()'))
    prescription_no = Column(String(255), nullable=False,unique=True, index=True)
    admission_id = Column(String(36),ForeignKey("inpatients.admission_id"),nullable=True)
    outpatient_id = Column(String(255), ForeignKey('outpatients.outpatient_id'), nullable=True)
    date_prescribed = Column(Date,nullable=False, default=text('NOW()'))
    patient_status = Column(String(255), nullable=True)
    status = Column(String(255),nullable=False, default="Unpaid")
    created_at = Column(DateTime,nullable=False, default=text('NOW()'))
    updated_at = Column(DateTime,nullable=True, default=text('NOW()'))

    inpatient_FK = relationship('Inpatient', foreign_keys=[admission_id])
    outpatient_Fk = relationship('Outpatient', foreign_keys=[outpatient_id])

class PrevDoctor(Base):
    __tablename__= 'prev_doctor'

    prev_did= Column(String(36), primary_key=True, default=text('UUID()'))
    medical_history_number = Column(String(255), ForeignKey('medical_history.medical_history_number'), nullable=True)
    doctor_name = Column(String(255), nullable=True) 
    created_at = Column(DateTime,nullable=False, default=text('NOW()'))
    updated_at = Column(DateTime,nullable=True, default=text('NOW()'))

    medical_history_fk = relationship("MedicalHistory", foreign_keys=[medical_history_number])

class PrevHospital(Base):
    __tablename__= 'prev_hospital'

    prev_hid= Column(String(36), primary_key=True, default=text('UUID()'))
    medical_history_number = Column(String(255), ForeignKey('medical_history.medical_history_number'), nullable=True)
    hospital_name = Column(String(255), nullable=True) 
    created_at = Column(DateTime,nullable=False, default=text('NOW()'))
    updated_at = Column(DateTime,nullable=True, default=text('NOW()'))

    medical_history_fk = relationship("MedicalHistory", foreign_keys=[medical_history_number])

class Room(Base):
    __tablename__ = 'rooms'

    room_id = Column(String(36), primary_key=True, default=text('UUID()'))
    room_number = Column(String(255), nullable=False)
    date_admitted = Column(DateTime, default=text('NOW()'))
    admission_id = Column(String(255), ForeignKey('inpatients.admission_id'), nullable=True)
    outpatient_id = Column(String(255), ForeignKey('outpatients.outpatient_id'), nullable=True)
    room_type_id = Column(String(36), nullable=True)
    location = Column(String(36), nullable=True)
    room_status = Column(String(36), nullable=False)
    active_status = Column(String(36), nullable=False)
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    # rooms_inpatientFk = relationship('Inpatient')
    room_inpatientFk = relationship('Inpatient', foreign_keys=[admission_id])
    room_outpatientFk = relationship('Outpatient', foreign_keys=[outpatient_id])


#*-----end of core------

#** FINANCE
#? BILLING
class HospitalServiceName(Base):
    __tablename__ = "hospital_service_name"
    id = Column(String(36), primary_key=True,index=True)
    description_name = Column(String(255),nullable=False,unique=True, index=True)
    unit_price = Column(Float, nullable=False)
    status = Column(String(100), default='Active')
    created_by = Column(String(36), ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime,nullable=False)
    updated_by = Column(String(36),ForeignKey("users.id"),nullable=True)
    updated_at = Column(DateTime,nullable=True)

class HospitalServices(Base):
    __tablename__ = "hospital_services"
    id = Column(String(36), primary_key=True,index=True)
    patient_id = Column(String(36), ForeignKey("patient_registration.patient_id"),nullable=False)
    hospital_service_name_id = Column(String(36), ForeignKey("hospital_service_name.id"),nullable=False)
    quantity= Column(Float,nullable=False)
    date= Column(Date, nullable=False)
    total_amount= Column(Float,nullable=False)
 
    status = Column(String(100), default='Pending',nullable=False) #nullable=False             ### STATUS TO FOR BILLING ###
    created_by = Column(String(36), ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime,nullable=False)
    updated_by = Column(String(36),ForeignKey("users.id"),nullable=True)
    updated_at = Column(DateTime,nullable=True)

    hc_treatment_services = relationship(
         "HospitalServiceName", primaryjoin="and_(HospitalServices.hospital_service_name_id==HospitalServiceName.id)")

    patient_info = relationship(
        "PatientRegistration", primaryjoin="and_(HospitalServices.patient_id==PatientRegistration.patient_id)")  #NEW1 PatientRegistration

class HospitalChargesBill(Base):
    __tablename__ = "hospital_charges_bill"
    id = Column(String(36), primary_key=True,index=True)
    invoice_no= Column(String(100) ,unique=True)
    invoice_date = Column(DateTime, nullable=False)
    inpatient_bill_id = Column(String(36), ForeignKey("inpatient_bills.id"),nullable=True)
    hospital_services_id = Column(String(36), ForeignKey("hospital_services.id"),nullable=False,unique=True)
    total_amount= Column(Float,nullable=False)
    cancellation_return = Column(Float, nullable=True)

    status = Column(String(100), default='Active')
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime (timezone=True), nullable=False, server_default=func.now())
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime (timezone=True), nullable=True, onupdate=func.now())   
    
    hospital_charges_id_info = relationship(
         "HospitalServices", primaryjoin="and_(HospitalChargesBill.hospital_services_id==HospitalServices.id)")  #NEW1 HospitalServices hospital_services_id

class TreatmentBill(Base):
    __tablename__ = "treatment_bill"
    id = Column(String(36), primary_key=True,index=True)
    invoice_no= Column(String(100) ,unique=True)
    invoice_date = Column(DateTime, nullable=False)
    inpatient_bill_id = Column(String(36), ForeignKey("inpatient_bills.id"),nullable=True)

    treatment_id = Column(String(36), ForeignKey("treatments.id"),nullable=False)
    total_amount= Column(Float,nullable=False)
    cancellation_return = Column(Float, nullable=True)

    status = Column(String(255), nullable=False, server_default="Pending")
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime (timezone=True), nullable=False, server_default=func.now())
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime (timezone=True), nullable=True, onupdate=func.now())   

    treatment_id_info = relationship(
         "Treatment", primaryjoin="and_(TreatmentBill.treatment_id==Treatment.id)")

class LabRequestBill(Base):
    __tablename__ = "lab_requests_bill"
    id = Column(String(36), primary_key=True,index=True)
    invoice_no= Column(String(100) ,unique=True)
    invoice_date = Column(DateTime, nullable=False)

    inpatient_bill_id = Column(String(36), ForeignKey("inpatient_bills.id"),nullable=True)

    lab_requests_id = Column(String(36), ForeignKey("lab_requests.id"),nullable=False)
    total_amount= Column(Float,nullable=False)
    cancellation_return = Column(Float, nullable=True)

    status = Column(String(255), nullable=False, server_default="Pending")
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime (timezone=True), nullable=False, server_default=func.now())
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime (timezone=True), nullable=True, onupdate=func.now())   

    lab_requests_id_info = relationship(
        "LabRequest", primaryjoin="and_(LabRequestBill.lab_requests_id==LabRequest.id)")

class PharmacyBill(Base):
    __tablename__ = "pharmacy_bill"
    id = Column(String(36), primary_key=True,index=True)
    invoice_no= Column(String(100) ,unique=True)
    invoice_date = Column(DateTime, nullable=False)

    inpatient_bill_id = Column(String(36), ForeignKey("inpatient_bills.id"),nullable=True)
    # pharmacy_invoice_id = Column(String(36), ForeignKey("pharmacy_invoice.id"),nullable=False) #NEW1 REMOVED COLUMN
    medicine_pr_id= Column(String(36),ForeignKey("medicine_pr.medpr_id"),nullable=False)  #NEW1 NEW COLUMN #medicalsupplies_pr
    total_amount= Column(Float,nullable=False)
    cancellation_return = Column(Float, nullable=True  , default=00)

    status = Column(String(255), nullable=False, server_default="Pending")
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime (timezone=True), nullable=False, server_default=func.now())
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime (timezone=True), nullable=True, onupdate=func.now())  

class RoomBill(Base):
    __tablename__ = "room_bill"    
    id = Column(String(36), primary_key=True)
    invoice_no = Column(String(100), nullable=False, unique=True)
    invoice_date = Column(DateTime, nullable=False)
    inpatient_id = Column(String(36), ForeignKey("inpatients.admission_id"), nullable=False) #NEW1 Deleted management
    inpatient_bill_id = Column(String(36), ForeignKey("inpatient_bills.id"), nullable=True)
    total_amount = Column(Float, nullable=False)

    status = Column(String(255), nullable=False, server_default="Pending")
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime (timezone=True), nullable=False, server_default=func.now())
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime (timezone=True), nullable=True, onupdate=func.now())   
    
    inpatient_management_id_info = relationship(
         "Inpatient", primaryjoin="and_(RoomBill.inpatient_id==Inpatient.admission_id)") #NEW1 Management deleted

class DoctorFeeBill(Base):
    __tablename__ = "doctor_fee_bill"
    id = Column(String(36), primary_key=True,index=True)
    invoice_no= Column(String(100) ,unique=True)
    invoice_date = Column(DateTime, nullable=False)

    inpatient_bill_id = Column(String(36), ForeignKey("inpatient_bills.id"),nullable=True)
    doctor_id = Column(String(36), ForeignKey("doctor_profile.doctor_id"),nullable=False)
    
    actual_pf = Column(Float,nullable=False)
    sc_pwd_discount = Column(Float, nullable=True)
    philhealth = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    hmo = Column(Float, nullable=True)
    patient_due = Column(Float, nullable=False)

    status = Column(String(100), default='Active')
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime (timezone=True), nullable=False, server_default=func.now())
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime (timezone=True), nullable=True, onupdate=func.now())   
    
class InpatientBill(Base):
    __tablename__ = "inpatient_bills"    
    id = Column(String(36), primary_key=True)
    inpatient_bill_no = Column(String(255), nullable=False, unique=True)
    admission_id = Column(String(36), ForeignKey("inpatients.admission_id"),nullable=False)
    inpatient_payment_id = Column(String(36), ForeignKey("inpatient_payments.id"),nullable=True)

    date_of_billing = Column(Date,nullable=False)
    due_date = Column(Date,nullable=False)
    balance_due = Column(Float, nullable=False, server_default="0")
    status = Column(String(255), nullable=False, server_default="Pending")
    created_by = Column(String(36), ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime (timezone=True), nullable=False, server_default=func.now())
    updated_by = Column(String(36),ForeignKey("users.id"),nullable=True)
    updated_at = Column(DateTime (timezone=True), nullable=True, onupdate=func.now())

    admission_info = relationship(
       "Inpatient", primaryjoin="and_(InpatientBill.admission_id==Inpatient.admission_id)")
    bill_treatments = relationship(
        "TreatmentBill", primaryjoin="and_(InpatientBill.id ==TreatmentBill.inpatient_bill_id)")
    bill_lab_requests = relationship(
        "LabRequestBill", primaryjoin="and_(InpatientBill.id ==LabRequestBill.inpatient_bill_id)")
    bill_pharmacy = relationship(
        "PharmacyBill", primaryjoin="and_(InpatientBill.id ==PharmacyBill.inpatient_bill_id)")
    bill_hospital_charges = relationship(
        "HospitalChargesBill", primaryjoin="and_(InpatientBill.id ==HospitalChargesBill.inpatient_bill_id)")
    bill_room = relationship(
        "RoomBill", primaryjoin="and_(InpatientBill.id ==RoomBill.inpatient_bill_id)")
    bill_doctor_fee = relationship(
        "DoctorFeeBill", primaryjoin="and_(InpatientBill.id ==DoctorFeeBill.inpatient_bill_id)")


#*-----end of finance-----

#** HUMAN RESOURCE

#? RECRUITMENT MANAGEMENT

# Applicant Model
class Applicant(Base):
    __tablename__ = "applicants"

    # ==================================================================================
    # Columns
    # ==================================================================================

    applicant_id = Column(String(36), primary_key = True, default = text('UUID()'))
    job_post_id = Column(String(36), ForeignKey("job_posts.job_post_id"), nullable = False)
    first_name = Column(String(255), nullable = False)
    middle_name = Column(String(255), nullable = True)
    last_name = Column(String(255), nullable = False)
    suffix_name = Column(String(255), nullable = True)
    resume = Column(String(255), nullable = False,unique = True)
    contact_number = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False)
    status = Column(String(255), nullable = False,default = "For evaluation")
    evaluated_by = Column(String(36), ForeignKey("employees.employee_id"), nullable = True)
    evaluated_at = Column(DateTime, nullable = True)
    screened_by = Column(String(36), ForeignKey("employees.employee_id"), nullable = True)
    screened_at = Column(DateTime, nullable = True)
    hired_by = Column(String(36), ForeignKey("employees.employee_id"), nullable = True)
    hired_at = Column(String(36), nullable = True)
    rejected_by = Column(String(36), ForeignKey("employees.employee_id"), nullable = True)
    rejected_at = Column(DateTime, nullable = True)
    remarks = Column(Text, nullable = True)
    created_at = Column(DateTime, default = text('NOW()'), nullable = False)
    updated_at = Column(DateTime, default = text('NOW()'), onupdate = text('NOW()'))

    # ==================================================================================
    # Relationships (From other tables/models)
    # ==================================================================================

    # From JobPost
    applied_job = relationship("JobPost", back_populates = "applicants")
    
    # From Employee
    applicant_evaluated_by = relationship(
        "Employee",
        back_populates = "evaluated_applicants",
        foreign_keys = "Applicant.evaluated_by"
    )
    applicant_screened_by = relationship(
        "Employee",
        back_populates = "screened_applicants",
        foreign_keys = "Applicant.screened_by"
    )
    applicant_hired_by = relationship(
        "Employee",
        back_populates = "hired_applicants",
        foreign_keys = "Applicant.hired_by"
    )
    applicant_rejected_by = relationship(
        "Employee",
        back_populates = "rejected_applicants",
        foreign_keys = "Applicant.rejected_by"
    )

    # ==================================================================================
    # Relationships (To other tables/models)
    # ==================================================================================

    # To Interviewee
    interviewee_info = relationship(
        "Interviewee",
        back_populates = "applicant_info",
        uselist = False
    )

# Department Model
# Hiram namin sa core human capital
class Department(Base):
    __tablename__ = "departments"

    # ==================================================================================
    # Columns
    # ==================================================================================

    department_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    name = Column(
        String(255),
        nullable = False
    )
    description = Column(
        String(255),
        nullable = False
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationships (To other tables)
    # ==================================================================================

    # To SubDepartment
    sub_departments = relationship(
        "SubDepartment",
        back_populates = "main_department"
    )

# Employee Model
# Hiram namin sa core human capital
class Employee(Base):
    __tablename__ = "employees"

    # ==================================================================================
    # Columns
    # ==================================================================================

    employee_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    first_name = Column(
        String(255),
        nullable = False
    )
    middle_name = Column(
        String(255),
        nullable =  True
    )
    last_name = Column(
        String(255),
        nullable = False
    )
    extension_name = Column(
        String(255),
        nullable = True
    )
    contact_number = Column(
        String(255),
        nullable = False
    )
    position_id = Column(
        String(36),
        ForeignKey("positions.position_id"),
        nullable = False
    )
    employment_type_id = Column(
        String(255),
        ForeignKey("employment_types.employment_type_id"),
        nullable = False
    )
    status = Column(
        String(255),
        nullable = True
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )


    # ==================================================================================
    # Relationships (From other tables)
    # ==================================================================================
    
    # From Position
    position = relationship(
        "Position",
        back_populates = "employees"
    )

    # From EmploymentType
    employment_type = relationship(
        "EmploymentType",
        back_populates = "employees"
    )


    # ==================================================================================
    # Relationships (To other tables)
    # ==================================================================================
    
    # To User
    user_credentials = relationship(
        "User",
        back_populates = "employee_info"
    )
    
    # To ManpowerRequst
    requested_manpower_requests = relationship(
        "ManpowerRequest", 
        back_populates = "manpower_request_requested_by",
        foreign_keys = "ManpowerRequest.requested_by"
    )
    signed_manpower_requests = relationship(
        "ManpowerRequest",
        back_populates = "manpower_request_signed_by",
        foreign_keys = "ManpowerRequest.signed_by"
    )
    reviewed_manpower_requests = relationship(
        "ManpowerRequest",
        back_populates = "manpower_request_reviewed_by",
        foreign_keys = "ManpowerRequest.reviewed_by"
    )
    rejected_manpower_requests = relationship(
        "ManpowerRequest",
        back_populates = "manpower_request_rejected_by",
        foreign_keys = "ManpowerRequest.rejected_by"
    )

    # To JobPost
    created_job_posts = relationship(
        "JobPost",
        back_populates = "job_post_posted_by"
    )

    # To JobCategory
    created_job_categories = relationship(
        "JobCategory",
        back_populates = "job_category_created_by"
    )

    # To Applicant
    evaluated_applicants = relationship(
        "Applicant",
        back_populates = "applicant_evaluated_by",
        foreign_keys = "Applicant.evaluated_by"
    )
    screened_applicants = relationship(
        "Applicant",
        back_populates = "applicant_screened_by",
        foreign_keys = "Applicant.screened_by"
    )
    hired_applicants = relationship(
        "Applicant",
        back_populates = "applicant_hired_by",
        foreign_keys = "Applicant.hired_by"
    )
    rejected_applicants = relationship(
        "Applicant",
        back_populates = "applicant_rejected_by",
        foreign_keys = "Applicant.rejected_by"
    )

    # To InterviewSchedule
    set_interview_schedules = relationship(
        "InterviewSchedule",
        back_populates = "interview_schedule_set_by" 
    )

    # To Interview Score
    set_interview_scores = relationship(
        "InterviewScore",
        back_populates = "interview_scored_by"
    )

    # To InterviewQuestion
    added_interview_questions = relationship(
        "InterviewQuestion",
        back_populates = "interview_question_added_by",
        foreign_keys = "InterviewQuestion.added_by"
    )
    updated_interview_questions = relationship(
        "InterviewQuestion",
        back_populates = "interview_question_updated_by",
        foreign_keys = "InterviewQuestion.updated_by"
    )

    # To OnboardingEmployee
    signed_onboarding_employees = relationship(
        "OnboardingEmployee",
        back_populates = "onboarding_employee_signed_by",
        foreign_keys = "OnboardingEmployee.signed_by"
    )
    updated_onboarding_employees = relationship(
        "OnboardingEmployee",
        back_populates = "onboarding_employee_updated_by",
        foreign_keys = "OnboardingEmployee.updated_by"
    )

    # To OnboardingTask
    added_onboarding_tasks = relationship(
        "OnboardingTask",
        back_populates = "onboarding_task_added_by",
        foreign_keys = "OnboardingTask.added_by"
    )
    updated_onboarding_tasks = relationship(
        "OnboardingTask",
        back_populates = "onboarding_task_updated_by",
        foreign_keys = "OnboardingTask.updated_by"
    )

    # To OnboardingEmployeeTask
    assigned_onboarding_employee_tasks = relationship(
        "OnboardingEmployeeTask",
        back_populates = "onboarding_employee_task_assigned_by",
        foreign_keys = "OnboardingEmployeeTask.assigned_by"
    )
    completed_onboarding_employee_tasks = relationship(
        "OnboardingEmployeeTask",
        back_populates = "onboarding_employee_task_completed_by",
        foreign_keys = "OnboardingEmployeeTask.completed_by"
    )


# Employment Type Model
# Hiram namin sa core human capital
class EmploymentType(Base):
    __tablename__ = "employment_types"

    # ==================================================================================
    # Column
    # ==================================================================================

    employment_type_id = Column(
        String(36),
        primary_key=True,
        default=text('UUID()')
    )
    name = Column(
        String(255),
        nullable = False
    )
    description = Column(
        Text,
        nullable = False,
    )
    is_active = Column(
        Boolean,
        default = True,
        nullable = False
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationship (To other tables/models)
    # ==================================================================================

    # To ManpoweRequest
    manpower_requests = relationship(
        "ManpowerRequest",
        back_populates = "employment_type"
    )

    # To Employee
    employees = relationship(
        "Employee",
        back_populates = "employment_type"
    )


# Interviewee Model
class Interviewee(Base):
    __tablename__ = "interviewees"

    # ==================================================================================
    # Columns
    # ==================================================================================

    interviewee_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    applicant_id = Column(
        String(36),
        ForeignKey("applicants.applicant_id"),
        nullable = False
    )
    interview_schedule_id = Column(
        String(36),
        ForeignKey("interview_schedules.interview_schedule_id"),
        nullable = True
    )
    is_interviewed = Column(
        Boolean,
        nullable = True
    )
    interviewed_at = Column(
        DateTime,
        nullable = True
    )
    remarks = Column(
        Text,
        nullable = True
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationships (From other tables/models)
    # ==================================================================================

    # From Applicant
    applicant_info = relationship(
        "Applicant",
        back_populates = "interviewee_info",
        uselist = False
    )

    # From InterviewSchedule
    interview_schedule = relationship(
        "InterviewSchedule",
        back_populates = "interviewees"
    )
    
    # ==================================================================================
    # Relationships (To other tables/models)
    # ==================================================================================

    # To InterviewScore
    interview_scores = relationship(
        "InterviewScore",
        back_populates = "score_for"
    )


# Interview Question Model
class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    # ==================================================================================
    # Columns
    # ==================================================================================

    interview_question_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    question = Column(
        String(255),
        nullable = False
    )
    type = Column(
        String(255),
        nullable = False
    )
    added_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = False
    )
    updated_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = True
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationships (From other tables/columns)
    # ==================================================================================

    # From Employee
    interview_question_added_by = relationship(
        "Employee",
        back_populates = "added_interview_questions",
        foreign_keys = "InterviewQuestion.added_by"
    )
    interview_question_updated_by = relationship(
        "Employee",
        back_populates = "updated_interview_questions",
        foreign_keys = "InterviewQuestion.updated_by"
    )

    # ==================================================================================
    # Relationships (To other tables/columns)
    # ==================================================================================
    
    # To InterviewScore
    interview_scores = relationship(
        "InterviewScore",
        back_populates = "interview_question"
    )


# Inteview Schedule Model
class InterviewSchedule(Base):
    __tablename__ = "interview_schedules"

    # ==================================================================================
    # Columns
    # ==================================================================================

    interview_schedule_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    job_post_id = Column(
        String(36),
        ForeignKey("job_posts.job_post_id"),
        nullable = False
    )
    scheduled_date = Column(
        Date,
        nullable = False
    )
    start_session = Column(
        Time,
        nullable = False
    )
    end_session = Column(
        Time,
        nullable = False
    )
    set_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = True
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationships (From other tables/columns)
    # ==================================================================================

    # From JobPost
    schedule_for = relationship(
        "JobPost",
        back_populates = "interview_schedules"
    )

    # From Employee
    interview_schedule_set_by = relationship(
        "Employee",
        back_populates = "set_interview_schedules"
    )

    # ==================================================================================
    # Relationships (To other tables/columns)
    # ==================================================================================

    # To Interviewees
    interviewees = relationship(
        "Interviewee",
        back_populates = "interview_schedule"
    )


# Interview Score Model
class InterviewScore(Base):
    __tablename__ = "interview_scores"

    # ==================================================================================
    # Columns
    # ==================================================================================

    interview_score_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    interviewee_id = Column(
        String(36),
        ForeignKey("interviewees.interviewee_id"),
        nullable = False
    )
    interview_question_id = Column(
        String(36),
        ForeignKey("interview_questions.interview_question_id")
    )
    score = Column(
        Float,
        nullable = True
    )
    scored_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = True
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationships (From other tables/columns)
    # ==================================================================================

    # From InterviewQuestion
    interview_question = relationship(
        "InterviewQuestion",
        back_populates = "interview_scores"
    )

    # From Employee
    interview_scored_by = relationship(
        "Employee",
        back_populates = "set_interview_scores"
    )

    # From Interviewee
    score_for = relationship(
        "Interviewee",
        back_populates = "interview_scores"
    )


# Job Category Model
class JobCategory(Base):
    __tablename__ = "job_categories"

    # ==================================================================================
    # Columns
    # ==================================================================================

    job_category_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    name = Column(
        String(36),
        nullable = False
    )
    description = Column(
        Text,
        nullable = False
    )
    is_removed = Column(
        Boolean,
        nullable = False,
        default = False
    )
    created_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = False
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationships (From other tables/models)
    # ==================================================================================

    # From Employee
    job_category_created_by = relationship(
        "Employee",
        back_populates = "created_job_categories",
    )

    # ==================================================================================
    # Relationships (To other tables/models)
    # ==================================================================================

    job_posts = relationship(
        "JobPost",
        back_populates = "job_category"
    )


# Job Post Model
class JobPost(Base):
    __tablename__ = "job_posts"

    # ==================================================================================
    # Columns
    # ==================================================================================

    job_post_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    manpower_request_id = Column(
        String(36),
        ForeignKey("manpower_requests.manpower_request_id"),
        nullable = False
    )
    is_salary_visible = Column(
        Boolean,
        nullable = False,
        default = False
    )
    content = Column(
        Text,
        nullable = False
    )
    expiration_date = Column(
        DateTime,
        nullable = True
    )
    job_category_id = Column(
        String(36),
        ForeignKey("job_categories.job_category_id"),
        nullable = False
    )
    posted_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = False
    )
    views = Column(
        Integer,
        nullable = False,
        default = 0
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationship (From other tables/models)
    # ==================================================================================

    # From ManpowerRequest
    manpower_request = relationship(
        "ManpowerRequest",
        back_populates = "job_post"
    )

    # From Employee
    job_post_posted_by = relationship(
        "Employee",
        back_populates = "created_job_posts"
    )

    # From JobCategory
    job_category = relationship(
        "JobCategory",
        back_populates = "job_posts",
    )

    # ==================================================================================
    # Relationship (To other tables/models)
    # ==================================================================================

    # To Applicants
    applicants = relationship(
        "Applicant",
        back_populates = "applied_job"
    )

    # To Interview Schedule
    interview_schedules = relationship(
        "InterviewSchedule",
        back_populates = "schedule_for"
    )


# Manpower Request Model
class ManpowerRequest(Base):
    __tablename__ = "manpower_requests"

    # ==================================================================================
    # Columns
    # ==================================================================================

    manpower_request_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    requisition_no = Column(
        String(255),
        unique = True,
        nullable = False
    )
    requested_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = False
    )
    position_id = Column(
        String(36),
        ForeignKey("positions.position_id"),
        nullable = False
    )
    employment_type_id = Column(
        String(255),
        ForeignKey("employment_types.employment_type_id"),
        nullable = False
    )
    request_nature = Column(
        String(255),
        default = "For Review",
        nullable = False
    )
    staffs_needed = Column(
        Integer,
        nullable = False
    )
    min_monthly_salary = Column(
        Float,
        nullable = True
    )
    max_monthly_salary = Column(
        Float,
        nullable = True
    )
    content = Column(
        Text,
        nullable = False
    )
    request_status = Column(
        String(255),
        nullable = False
    )
    deadline = Column(
        DateTime,
        nullable = True
    )
    signed_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = True
    )
    signed_at = Column(
        DateTime,
        nullable = True
    )
    reviewed_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = True
    )
    reviewed_at = Column(
        DateTime,
        nullable = True
    )
    completed_at = Column(
        DateTime,
        nullable = True
    )
    rejected_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = True
    )
    rejected_at = Column(
        DateTime,
        nullable = True
    )
    remarks = Column(
        Text,
        nullable = True
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationship (From other tables/models)
    # ==================================================================================

    # From Employee
    manpower_request_requested_by = relationship(
        "Employee",
        back_populates = "requested_manpower_requests",
        foreign_keys = "ManpowerRequest.requested_by"
    )
    manpower_request_reviewed_by = relationship(
        "Employee",
        back_populates = "reviewed_manpower_requests",
        foreign_keys = "ManpowerRequest.reviewed_by"
    )
    manpower_request_signed_by = relationship(
        "Employee",
        back_populates = "signed_manpower_requests",
        foreign_keys = "ManpowerRequest.signed_by"
    )
    manpower_request_rejected_by = relationship(
        "Employee",
        back_populates = "rejected_manpower_requests",
        foreign_keys = "ManpowerRequest.rejected_by"
    )

    # From Employment Type
    employment_type = relationship(
        "EmployeeType",
        back_populates="manpower_requests",
    )

    # From EmploymentType
    employment_type = relationship(
        "EmploymentType",
        back_populates = "manpower_requests"
    )

    # From Position
    vacant_position = relationship(
        "Position",
        back_populates = "manpower_requests"
    )

    # ==================================================================================
    # Relationship (To other tables/models)
    # ==================================================================================

    # To JobPost
    job_post = relationship(
        "JobPost",
        back_populates = "manpower_request",
        uselist = False
    )


# Onboarding Employee Model
class OnboardingEmployee(Base):
    __tablename__ = "onboarding_employees"

    # ==================================================================================
    # Columns
    # ==================================================================================

    onboarding_employee_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    first_name = Column(
        String(255),
        nullable = False
    )
    middle_name = Column(
        String(255),
        nullable = True
    )
    last_name = Column(
        String(255),
        nullable = False
    )
    suffix_name = Column(
        String(255),
        nullable = True
    )
    contact_number = Column(
        String(255),
        nullable = False
    )
    email = Column(
        String(255),
        nullable = False
    )
    position_id = Column(
        String(36),
        ForeignKey("positions.position_id"),
        nullable = False
    )
    employment_start_date = Column(
        Date,
        nullable = True
    )
    employment_contract = Column(
        String(255),
        unique = True,
        nullable = False
    )
    status = Column(
        String(255),
        nullable = False
    )
    signed_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = False
    )
    updated_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = True
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationship (From other tables/models)
    # ==================================================================================

    # From Position
    onboarding_employee_position = relationship(
        "Position",
        back_populates = "onboarding_employees"
    )

    # From Employee
    onboarding_employee_signed_by = relationship(
        "Employee",
        back_populates = "signed_onboarding_employees",
        foreign_keys = "OnboardingEmployee.signed_by"
    )
    onboarding_employee_updated_by = relationship(
        "Employee",
        back_populates = "updated_onboarding_employees",
        foreign_keys = "OnboardingEmployee.updated_by"
    )

    # ==================================================================================
    # Relationship (To other tables/models)
    # ==================================================================================

    # To OnboardingEmployeeTask
    onboarding_employee_tasks = relationship(
        "OnboardingEmployeeTask",
        back_populates = "onboarding_employee"
    )


# Onboarding Employye Task Model
class OnboardingEmployeeTask(Base):
    __tablename__ = "onboarding_employee_task"
    
    # ==================================================================================
    # Columns
    # ==================================================================================

    onboarding_employee_task_id = Column(
        String(36),
        primary_key = True,
        default = text("UUID()")
    )
    onboarding_employee_id = Column(
        String(36),
        ForeignKey("onboarding_employees.onboarding_employee_id"),
        nullable = False
    )
    onboarding_task_id = Column(
        String(36),
        ForeignKey("onboarding_tasks.onboarding_task_id"),
        nullable = False
    )
    start_at = Column(
        DateTime,
        nullable = False
    )
    end_at = Column(
        DateTime,
        nullable = False
    )
    assigned_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = False
    )
    status = Column(
        String(255),
        nullable = False
    )
    completed_at = Column(
        DateTime,
        nullable = True
    )
    completed_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = True
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationships (From other tables/models)
    # ==================================================================================

    # From OnboardingEmployee
    onboarding_employee = relationship(
        "OnboardingEmployee",
        back_populates = "onboarding_employee_tasks"
    )

    # From OnboardingTask
    onboarding_task = relationship(
        "OnboardingTask",
        back_populates = "assigned_tasks"
    )
    
    # From Employee
    onboarding_employee_task_assigned_by = relationship(
        "Employee",
        back_populates = "assigned_onboarding_employee_tasks",
        foreign_keys = "OnboardingEmployeeTask.assigned_by"
    )
    onboarding_employee_task_completed_by = relationship(
        "Employee",
        back_populates = "completed_onboarding_employee_tasks",
        foreign_keys = "OnboardingEmployeeTask.completed_by"
    )


# Onboarding Tasks Model
class OnboardingTask(Base):
    __tablename__ = "onboarding_tasks"

    # ==================================================================================
    # Columns
    # ==================================================================================

    onboarding_task_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    title = Column(
        String(255),
        nullable = False
    )
    description = Column(
        Text,
        nullable = False
    )
    task_type = Column(
        String(255),
        nullable = False
    )
    is_general = Column(
        Boolean,
        nullable = False,
        default = False
    )
    sub_department_id = Column(
        String(36),
        ForeignKey("sub_departments.sub_department_id"),
        nullable = False
    )
    added_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = False
    )
    updated_by = Column(
        String(36),
        ForeignKey("employees.employee_id"),
        nullable = True
    )
    is_deleted = Column(
        Boolean,
        nullable = False,
        default = False
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationship (From other tables/column)
    # ==================================================================================

    # From SubDepartment
    for_sub_department = relationship(
        "SubDepartment",
        back_populates = "onboarding_tasks"
    )

    # Employee
    onboarding_task_added_by = relationship(
        "Employee",
        back_populates = "added_onboarding_tasks",
        foreign_keys = "OnboardingTask.added_by"
    )
    onboarding_task_updated_by = relationship(
        "Employee",
        back_populates = "updated_onboarding_tasks",
        foreign_keys = "OnboardingTask.updated_by"
    )

    # ==================================================================================
    # Relationship (To other tables/column)
    # ==================================================================================

    # To OnboardingEmployeeTask
    assigned_tasks = relationship(
        "OnboardingEmployeeTask",
        back_populates = "onboarding_task"
    )


# Position Model
# Hiram namin sa core human capital
class Position(Base):
    __tablename__ = "positions"

    # ==================================================================================
    # Columns
    # ==================================================================================

    position_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()'),
    )
    sub_department_id = Column(
        String(36),
        ForeignKey("sub_departments.sub_department_id"),
        nullable = False
    )
    name = Column(
        String(255),
        nullable = False
    )
    description = Column(
        String(255),
        nullable = False
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationship (From other tables/models)
    # ==================================================================================

    # From SubDepartment
    sub_department = relationship(
        "SubDepartment",
        back_populates = "positions"
    )

    # ==================================================================================
    # Relationship (To other tables/models)
    # ==================================================================================

    # To Employee
    employees = relationship(
        "Employee",
        back_populates = "position"
    )

    # To ManpowerRequest
    manpower_requests = relationship(
        "ManpowerRequest",
        back_populates = "vacant_position"
    )

    # To OnboardingEmployee
    onboarding_employees = relationship(
        "OnboardingEmployee",
        back_populates = "onboarding_employee_position"
    )


# Sub Department Model
# Hiram namin sa core human capital
class SubDepartment(Base):
    __tablename__ = "sub_departments"

    # ==================================================================================
    # Columns
    # ==================================================================================

    sub_department_id = Column(
        String(36),
        primary_key = True,
        default = text('UUID()')
    )
    department_id = Column(
        String(36),
        ForeignKey("departments.department_id"),
        nullable = False
    )
    name = Column(
        String(255),
        nullable = False
    )
    description = Column(
        Text,
        nullable = False
    )
    location = Column(
        String(255),
        nullable = False
    )
    created_at = Column(
        DateTime,
        default = text('NOW()'),
        nullable = False
    )
    updated_at = Column(
        DateTime,
        default = text('NOW()'),
        onupdate = text('NOW()')
    )

    # ==================================================================================
    # Relationship (From other tables/models)
    # ==================================================================================

    # From department
    main_department = relationship(
        "Department",
        back_populates = "sub_departments"
    )

    # ==================================================================================
    # Relationship (From other tables/models)
    # ==================================================================================

    # To Position
    positions = relationship(
        "Position", 
        back_populates = "sub_department"
    )

    # To OnboardingTask
    onboarding_tasks = relationship(
        "OnboardingTask",
        back_populates = "for_sub_department"
    )


#? TIME AND ATTENDANCE
class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    employee_id = Column(String(36), ForeignKey('employees.id'), nullable=False)
    time_in_id = Column(String(36), ForeignKey('time_ins.id'), nullable=False)
    time_out_id = Column(String(36), ForeignKey('time_outs.id'), nullable=False)
    hours_worked = Column(String(36), nullable=False)
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    employees = relationship('Employee', back_populates='attendances', lazy='joined')
    time_ins = relationship('TimeIn', back_populates='attendances', lazy='joined')
    time_outs = relationship('TimeOut', back_populates='attendances', lazy='joined')

#! PAKIAYOS LAHAT NG MAY EMPLOYEE HEHE
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
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
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

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

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    title = Column(String(255), nullable=False)
    number_of_days = Column(String(255), nullable=False)
    active_status = Column(String(255), nullable=True, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    employees = relationship('Employee', back_populates='employee_status')

#* used by: Procurement
class EmployeeType(Base):
    __tablename__ = 'employee_types'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    title = Column(String(255), nullable=False)
    active_status = Column(String(255), nullable=True, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    employees = relationship('Employee', back_populates='employee_types')

class Leave(Base):
    __tablename__ = 'leaves'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    employee_id = Column(String(36), ForeignKey('employees.id'), nullable=False)
    leave_type_id = Column(String(36), ForeignKey('leave_types.id'), nullable=False)
    leave_sub_type_id = Column(String(36), ForeignKey('leave_sub_types.id'), nullable=False)
    title = Column(String(255), nullable=False)
    reason = Column(String(500), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(255), nullable=False, server_default=text("'Pending'"))
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    leave_types = relationship('LeaveType', back_populates='leaves', lazy='joined')
    employees = relationship('Employee', back_populates='leaves', lazy='joined')
    leave_sub_types = relationship('LeaveSubType', back_populates='leaves', lazy='joined')

class LeaveSubType(Base):
    __tablename__ = 'leave_sub_types'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    title = Column(String(255), nullable=False)
    number_of_days = Column(String(255), nullable=False)
    leave_type_id = Column(String(36), ForeignKey('leave_types.id'), nullable=False)
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    leave_types = relationship('LeaveType', back_populates='leave_sub_types', lazy='joined')
    leaves = relationship('Leave', back_populates='leave_sub_types')

class LeaveType(Base):
    __tablename__ = 'leave_types'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    title = Column(String(255), nullable=False)
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    leaves = relationship('Leave', back_populates='leave_types')
    leave_sub_types = relationship('LeaveSubType', back_populates='leave_types')

class MissedTime(Base):
    __tablename__ = 'missed_times'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    employee_id = Column(String(36), ForeignKey('employees.id'), nullable=False)
    approved_by = Column(String(36), ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    time_log = Column(Time, nullable=False)
    time_log_type = Column(String(255), nullable=False)
    proof = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False, server_default=text("'Pending'"))
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    employees = relationship('Employee', back_populates='missed_times', lazy='joined')
    users = relationship('User', back_populates='missed_times', lazy='joined')

class ShiftChange(Base):
    __tablename__ = 'shift_changes'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
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
    status = Column(String(255), nullable=False, server_default=text("'Pending'"))
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))


    employees = relationship('Employee', back_populates='shift_changes', lazy='joined')
    shift_types = relationship('ShiftType', back_populates='shift_changes', lazy='joined')

class ShiftType(Base):
    __tablename__ = 'shift_types'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    title = Column(String(255), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    employees = relationship('Employee', back_populates='shift_types')
    shift_changes = relationship('ShiftChange', back_populates='shift_types')

class TimeIn(Base):
    __tablename__ = 'time_ins'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    time_log = Column(Time, nullable=False)
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    employees = relationship('Employee', back_populates='time_ins', lazy='joined')
    attendances = relationship('Attendance', back_populates='time_ins')

class TimeOut(Base):
    __tablename__ = 'time_outs'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    time_log = Column(Time, nullable=False)
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    employees = relationship('Employee', back_populates='time_outs', lazy='joined')
    attendances = relationship('Attendance', back_populates='time_outs')
#*------end of human resource------

#* LOGISTICS
#? ASSET MANAGEMENT
class Asset(Base):
    __tablename__ = 'assets'

    asset_id = Column(String(60), primary_key=True, default=text('UUID()'))
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
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))
    created_by = Column(String(60), ForeignKey('users.user_id'))

    asset_provider = relationship('Asset_provider', back_populates='asset', lazy='joined')
    asset_type = relationship('Asset_Type', back_populates='asset', lazy='joined')
    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Asset_provider(Base):
    __tablename__ = 'asset_providers'

    asset_provider_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_provider_name = Column(String(255), nullable=True)
    asset_provider_contact = Column(String(255), nullable=True)
    asset_provider_email = Column(String(255), nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    asset = relationship('Asset')

class Asset_Type(Base):
    __tablename__ = 'asset_types'

    asset_type_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_type_title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    asset = relationship('Asset')

class Asset_Warranty(Base):
    __tablename__ = 'asset_warranty'

    warranty_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    warranty_length = Column(Numeric, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    warranty_contact = Column(String(255), nullable=True)
    warranty_email = Column(String(255), nullable=True)
    warranty_note = Column(String(255), nullable=True)
    active_status = Column(Text, nullable=True, default=('Active'))

    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))
    created_by = Column(String(36), ForeignKey('users.user_id'), nullable=True)

    asset_type = relationship('Asset', foreign_keys=[asset_id], lazy='joined')
    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Broken_Asset(Base):
    __tablename__ = 'broken_assets'

    broken_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    remarks = Column(Text, nullable=True)
    broken_date = Column(DateTime, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    created_by = Column(String(60), ForeignKey('users.user_id'))


    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Asset_check_in(Base):
    __tablename__ = 'asset_check_in'

    check_in_id = Column(String(36), primary_key=True, default=text('UUID()'))
    check_out_id = Column(String(60), ForeignKey('asset_check_out.check_out_id'), nullable=True)
    return_date = Column(DateTime, nullable=True)
    return_location = Column(String(255), nullable=True)
    remarks = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))
    
    check_out_details = relationship('Asset_check_out', foreign_keys=[check_out_id], lazy='joined')

class Asset_check_out(Base):
    __tablename__ = 'asset_check_out'

    check_out_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_id = Column(String(60), ForeignKey('assets.asset_id'), nullable=True)
    user_id = Column(String(60), ForeignKey('users.user_id'), nullable=True)
    department_id = Column(String(60), ForeignKey('department.department_id'), nullable=True)
    location = Column(String(255), nullable=True)
    check_out_date = Column(DateTime, nullable=True)
    check_out_due = Column(DateTime, nullable=True)
    remarks = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))
   
    on_department = relationship('Department', foreign_keys=[department_id], lazy='joined')
    on_user = relationship('User', foreign_keys=[user_id], lazy='joined')
    the_asset = relationship('Asset', foreign_keys=[asset_id], lazy='joined')

#* para saang department (asset? staff? patient? doctor?)
class Department(Base):
    __tablename__ = 'department'

    department_id = Column(String(36), primary_key=True, default=text('UUID()'))
    department_name = Column(String(255), nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))

class Dispose_Asset(Base):
    __tablename__ = 'dispose_assets'

    dispose_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    remarks = Column(Text, nullable=True)
    dispose_to = Column(String(255), nullable=True)
    dispose_date = Column(DateTime, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    created_by = Column(String(60), ForeignKey('users.user_id'))


    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Events(Base):
    __tablename__ = 'events'

    event_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    event_title = Column(String(255), nullable=True)
    event_message = Column(String(255), nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

class Maintenance(Base):
    __tablename__ = 'maintenances'

    maintenance_id = Column(String(36), primary_key=True, default=text('UUID()'))
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
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    Maintenance_provider = relationship('Maintenance_provider', back_populates='maintenance', lazy='joined')

class Maintenance_provider(Base):
    __tablename__ = 'maintenance_providers'

    maintenance_provider_id = Column(String(36), primary_key=True, default=text('UUID()'))
    maintenance_provider_name = Column(String(255), nullable=True)
    maintenance_provider_contact = Column(String(255), nullable=True)
    maintenance_provider_email = Column(String(255), nullable=True) 
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    maintenance = relationship('Maintenance')

class Maintenance_Report(Base):
    __tablename__ = 'maintenance_reports'

    maintenance_report_id = Column(String(36), primary_key=True, default=text('UUID()'))
    maintenance_id = Column(String(36), ForeignKey('maintenances.maintenance_id'), nullable=False)
    maintenance_cost = Column(Numeric, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    maintenance_details = relationship('Maintenance', foreign_keys=[maintenance_id], lazy='joined')

class Missing_Asset(Base):
    __tablename__ = 'missing_assets'

    missing_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    remarks = Column(Text, nullable=True)
    missing_date = Column(DateTime, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    created_by = Column(String(60), ForeignKey('users.user_id'))


    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Repair_Asset(Base):
    __tablename__ = 'repair_assets'

    repair_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    assigned_to = Column(String(255), nullable=True)
    repair_date = Column(DateTime, nullable=True)
    repair_price = Column(Numeric, nullable=True)
    remarks = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    created_by = Column(String(60), ForeignKey('users.user_id'))


    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')

class Request_Asset(Base):
    __tablename__ = 'request_assets'

    request_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_type_id = Column(String(36), ForeignKey('asset_types.asset_type_id'), nullable=True)
    request_brand = Column(String(255), nullable=True)
    request_model = Column(DateTime, nullable=True)
    request_description = Column(Text, nullable=True)
    request_status = Column(String(255), nullable=True)
    request_remark = Column(Text, nullable=True)
    active_status = Column(Text, nullable=True, default=('Active'))

    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))
    created_by = Column(String(36), ForeignKey('users.user_id'), nullable=True)
    updated_by = Column(String(36), ForeignKey('users.user_id'), nullable=True)

    asset_type = relationship('Asset_Type', lazy='joined')
    created_by_details = relationship('User', foreign_keys=[created_by], lazy='joined')
    updated_by_details = relationship('User', foreign_keys=[updated_by], lazy='joined')

class Sell_Asset(Base):
    __tablename__ = 'sell_assets'

    sell_id = Column(String(36), primary_key=True, default=text('UUID()'))
    asset_id = Column(String(36), ForeignKey('assets.asset_id'), nullable=True)
    sell_to = Column(String(255), nullable=True)
    sell_to_contact = Column(String(255), nullable=True)
    sell_to_email = Column(String(255), nullable=True)
    sell_date = Column(DateTime, nullable=True)
    sell_price = Column(Numeric, nullable=True)
    remarks = Column(Text, nullable=True)
    active_status = Column(String(255), nullable=True, default=('Active'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

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
    

    # relation with purchase_order
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

#? WAREHOUSE MANAGEMENT
# SAME class in T&A (Emplyee Table)
class Employees(Base):

    __tablename__ = 'employees'


    employee_id             = Column(String(36), primary_key=True, default=text('UUID()'))
    user_type               = Column(String(255), nullable=False)
    employee_first_name     = Column(String(255), nullable=False)
    employee_middle_name    = Column(String(255), nullable=True)
    employee_last_name      = Column(String(255), nullable=False)
    employee_contact        = Column(String(255), nullable=False, unique=True)
    employee_age            = Column(Integer, nullable=False)
    employee_address        = Column(String(255), nullable=False)

    created_at              = Column(DateTime, default=text('NOW()'))
    updated_at              = Column(DateTime, onupdate=text('NOW()'))


    user_id                 = Column(String(36), ForeignKey('users.user_id'), nullable=True, unique=True)
    
    employee_user = relationship('Users', backref='user_employeeFK')

    #Relationship/s of this Table to other Table/s
    or_employeeFK = relationship("Outbound_Reports", back_populates="employee")
    ir_employeeFK = relationship("Inbound_Reports", back_populates="emp")
    w_employeeFK = relationship("Warehouses", back_populates="manager")
    hd_employeeFK = relationship("Hospital_Departments", back_populates="manager")

# I think Same 'to ng ibang Departments na table sa ibang system 
class Hospital_Departments(Base):

    __tablename__ = 'hospital_departments'


    hospital_department_id              = Column(String(36), primary_key=True, default=text('UUID()'))
    hospital_department_name            = Column(String(255), nullable=False)
    hospital_department_description     = Column(Text, nullable=False)
    # hospital_manager                    = Column(String(255), nullable=False, default="Qura (Subject to Change)")

    created_at                          = Column(DateTime, default=text('NOW()'))
    updated_at                          = Column(DateTime, onupdate=text('NOW()'))


    hospital_manager_id                 = Column(String(36), ForeignKey('employees.employee_id'), nullable=True, unique=True)

 #Relationship/s
     #Relationship/s of this Table
    manager = relationship('Employees', back_populates='hd_employeeFK')

    #Relationship/s of this Table to other Table/s
    or_hospital_departmentFK = relationship('Outbound_Reports', back_populates='hospital_department')

class Inbound_Reports(Base):

    __tablename__ = 'inbound_reports'


    inbound_report_id           = Column(String(36), primary_key=True, default=text('UUID()'))
    status                      = Column(String(255), nullable=False)
    # total_quantity              = Column(INTEGER(20), nullable=False)

    created_at                  = Column(DateTime, default=text('NOW()'))
    updated_at                  = Column(DateTime, onupdate=text('NOW()'))


    request_id                  = Column(String(36), ForeignKey('request.request_id'), nullable=True)
    employee_id                 = Column(String(36), ForeignKey('employees.employee_id'), nullable=True)

    requested = relationship('Request', back_populates='ir_requestFK')
    emp = relationship('Employees', back_populates='ir_employeeFK')

class Inventory_Locations(Base):

    __tablename__ = 'inventory_locations'

    inventory_location_id           = Column(String(36), primary_key=True, default=text('UUID()'))
    inventory_location_name         = Column(String(255), nullable=False, unique=True)

    created_at                      = Column(DateTime, default=text('NOW()'))
    updated_at                      = Column(DateTime, onupdate=text('NOW()'))

    supply_category_id              = Column(String(36), ForeignKey('supply_categories.supply_category_id'), nullable=False)

    inventory_location_category = relationship("Supply_Categories", back_populates="il_supply_categoryFK")

    #Relationship/s of this Table to other Table/s
    inventory_ilFK = relationship("Inventories", back_populates="inventory_location")
    
class Inventories(Base):

    __tablename__ = 'inventories'


    inventory_id                    = Column(String(36), primary_key=True, default=text('UUID()'))

    created_at                      = Column(DateTime, default=text('NOW()'))
    updated_at                      = Column(DateTime, onupdate=text('NOW()'))

    inventory_location_id           = Column(String(36), ForeignKey('inventory_locations.inventory_location_id'), nullable=True)
    supply_id                       = Column(String(36), ForeignKey('supplies.supply_id'), nullable=True, unique=True)
    
    inventory_location = relationship("Inventory_Locations", back_populates="inventory_ilFK")
    inventory_supply = relationship("Supplies", back_populates="inventory_suppliesFK")

    #Relationship/s of this Table to other Table/sss
    ord_inventoryFK = relationship("Outbound_Report_Details", back_populates="inventory")
    
#* used by procurement
class Notifications(Base):

    __tablename__ = 'notifications'


    notification_id                 = Column(String(36), primary_key=True, default=text('UUID()'))
    description                     = Column(String(255), nullable=True)
    status                          = Column(String(255), nullable=False, default="Pending")

    created_at                      = Column(DateTime, default=text('NOW()'))
    updated_at                      = Column(DateTime, onupdate=text('NOW()'))

    supply_id                       = Column(String(36), ForeignKey('supplies.supply_id'), nullable=True, unique=True)
    request_id                      = Column(String(36), ForeignKey('request.request_id'), nullable=True, unique=True)
    return_id                       = Column(String(36), ForeignKey('return.return_id'), nullable=True, unique=True)

    
    supply_notif = relationship("Supplies", back_populates="notif_supplesFK")
    request_notif = relationship("Request", back_populates="notif_requestFK")
    return_notif = relationship("Return", back_populates="notif_returnFK")

class Outbound_Report_Details(Base):

    __tablename__ = 'outbound_report_details'


    outbound_r_details_id       = Column(String(36), primary_key=True, default=text('UUID()'))
    status                      = Column(String(255), nullable=False)
    quantity                    = Column(Integer(20), nullable=False)

    created_at                  = Column(DateTime, default=text('NOW()'))
    updated_at                  = Column(DateTime, onupdate=text('NOW()'))

    outbound_report_id          = Column(String(36), ForeignKey('outbound_reports.outbound_report_id'), nullable=True)
    inventory_id                = Column(String(36), ForeignKey('inventories.inventory_id'), nullable=True)

    outbound_report = relationship('Outbound_Reports', back_populates='ord_outbound_reportFK')
    inventory = relationship('Inventories', back_populates='ord_inventoryFK')

class Outbound_Reports(Base):

    __tablename__ = 'outbound_reports'


    outbound_report_id          = Column(String(36), primary_key=True, default=text('UUID()'))
    status                      = Column(String(255), nullable=False)
    total_quantity              = Column(Integer(20), nullable=False)
    expected_shipment_date      = Column(DateTime(255), nullable=False)
    complete_shipment_date      = Column(DateTime(255), nullable=True)

    created_at                  = Column(DateTime, default=text('NOW()'))
    updated_at                  = Column(DateTime, onupdate=text('NOW()'))

    hospital_department_id      = Column(String(36), ForeignKey('hospital_departments.hospital_department_id'), nullable=True)
    employee_id                 = Column(String(36), ForeignKey('employees.employee_id'), nullable=True)

    hospital_department = relationship('Hospital_Departments', back_populates='or_hospital_departmentFK')
    employee = relationship('Employees', back_populates='or_employeeFK')

    #Relationship/s of this Table to other Table/s
    ord_outbound_reportFK = relationship("Outbound_Report_Details", back_populates="outbound_report")

class Request_Details(Base):

    __tablename__ = 'request_details'


    request_details_id          = Column(String(36), primary_key=True, default=text('UUID()'))
    quantity                    = Column(Integer(20), nullable=False)
    status                      = Column(String(255), nullable=False, default="Pending")

    created_at                  = Column(DateTime, default=text('NOW()'))
    updated_at                  = Column(DateTime, onupdate=text('NOW()'))

    request_id                  = Column(String(36), ForeignKey('request.request_id'), nullable=True)
    supply_id                   = Column(String(36), ForeignKey('supplies.supply_id'), nullable=True)

    request = relationship('Request', back_populates='rd_requestFK')
    supply = relationship('Supplies', back_populates='rd_suppliesFK')

class Request(Base):

    __tablename__ = 'request'

    request_id                  = Column(String(36), primary_key=True, default=text('UUID()'))
    request_date                = Column(DateTime(255), nullable=False, default=text('NOW()'))
    requestor                   = Column(String(255), nullable=False)
    request_type                = Column(String(255), nullable=False)
    request_status              = Column(String(255), nullable=False, default="Pending")

    created_at                  = Column(DateTime, default=text('NOW()'))
    updated_at                  = Column(DateTime, onupdate=text('NOW()'))

    rd_requestFK = relationship('Request_Details', back_populates='request')
    ir_requestFK = relationship('Inbound_Reports', back_populates='requested')
    notif_requestFK = relationship("Notifications", back_populates="request_notif")

class Return_Details(Base):

    __tablename__ = 'return_details'


    return_detail_id            = Column(String(36), primary_key=True, default=text('UUID()'))
    quantity                    = Column(Integer(20), nullable=False)
    status                      = Column(String(255), nullable=False, default="Pending")

    created_at                  = Column(DateTime, default=text('NOW()'))
    updated_at                  = Column(DateTime, onupdate=text('NOW()'))

    return_id                   = Column(String(36), ForeignKey('return.return_id'), nullable=True)
    supply_id                   = Column(String(36), ForeignKey('supplies.supply_id'), nullable=True)

    returns = relationship('Return', back_populates='retd_returnFK')
    return_supply = relationship('Supplies', back_populates='retd_suppliesFK')

class Return(Base):

    __tablename__ = 'return'

    return_id                   = Column(String(36), primary_key=True, default=text('UUID()'))
    return_date                 = Column(DateTime(255), nullable=False)
    returner                    = Column(String(255), nullable=False)
    return_type                 = Column(String(255), nullable=False)
    return_status               = Column(String(255), nullable=False, default="Pending")

    created_at                  = Column(DateTime, default=text('NOW()'))
    updated_at                  = Column(DateTime, onupdate=text('NOW()'))

    retd_returnFK = relationship('Return_Details', back_populates='returns')
    notif_returnFK = relationship("Notifications", back_populates="return_notif")

class Suppliers(Base):
    __tablename__ = 'suppliers'

    supplier_id                     = Column(String(36), primary_key=True, default=text('UUID()'))
    supplier_name                   = Column(String(255), nullable=False)
    supplier_contact                = Column(String(255), nullable=False, unique=True)
    supplier_email                  = Column(String(255), nullable=False, unique=True)
    supplier_description            = Column(Text, nullable=False)

    created_at                      = Column(DateTime, default=text('NOW()'))
    updated_at                      = Column(DateTime, onupdate=text('NOW()'))

    #Relationship/s
    s_supplierFK = relationship("Supplies", back_populates="supply_supplier")

class Supply_Categories(Base):

    __tablename__ = 'supply_categories'


    supply_category_id              = Column(String(36), primary_key=True, default=text('UUID()'))
    supply_category_name            = Column(String(255), nullable=False, unique=True)
    supply_category_description     = Column(Text, nullable=True)

    created_at                      = Column(DateTime, default=text('NOW()'))
    updated_at                      = Column(DateTime, onupdate=text('NOW()'))

    il_supply_categoryFK = relationship('Inventory_Locations', back_populates='inventory_location_category')
    s_supply_categoryFK = relationship('Supplies', back_populates='supply_category')

class Supplies(Base):

    __tablename__ = 'supplies'


    supply_id                       = Column(String(36), primary_key=True, default=text('UUID()'))
    supply_name                     = Column(String(255), nullable=False)
    supply_quantity                 = Column(Integer(20), nullable=False)
    supply_unit_type                = Column(String(255), nullable=False)
    supply_unit_cost                = Column(DECIMAL, nullable=False)
    supply_description              = Column(Text, nullable=False)
    supply_reorder_interval         = Column(String(255), nullable=False)
    supply_expiration               = Column(DateTime(255), nullable=True)
    supply_status                   = Column(String(255), nullable=True, default="Good")

    created_at                      = Column(DateTime, default=text('NOW()'))
    updated_at                      = Column(DateTime, onupdate=text('NOW()'))

    supplier_id                     = Column(String(36), ForeignKey('suppliers.supplier_id'), nullable=True)
    supply_category_id              = Column(String(36), ForeignKey('supply_categories.supply_category_id'), nullable=True)

    supply_supplier = relationship("Suppliers", back_populates="s_supplierFK")
    supply_category = relationship("Supply_Categories", back_populates="s_supply_categoryFK")

    #Relationship/s of this Table to other Table/s
    inventory_suppliesFK = relationship("Inventories", back_populates="inventory_supply")
    notif_supplesFK = relationship("Notifications", back_populates="supply_notif")
    rd_suppliesFK = relationship("Request_Details", back_populates="supply")
    retd_suppliesFK = relationship("Return_Details", back_populates="return_supply")

class Warehouses(Base):

    __tablename__ = 'warehouses'


    warehouse_id                = Column(String(36), primary_key=True, default=text('UUID()'))
    warehouse_name              = Column(String(255), nullable=False)
    warehouse_description       = Column(Text, nullable=False)
    warehouse_address           = Column(String(255), nullable=False)
    warehouse_contact           = Column(String(255), nullable=False, unique=True)

    created_at                  = Column(DateTime, default=text('NOW()'))
    updated_at                  = Column(DateTime, onupdate=text('NOW()'))
    
    warehouse_manager_id        = Column(String(36), ForeignKey('employees.employee_id'), nullable=True, unique=True)

    manager = relationship('Employees', back_populates='w_employeeFK')

    #** FINANCE
    #? COLLECTION/DISBURSEMENT

    














































































