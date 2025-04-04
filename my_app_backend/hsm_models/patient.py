from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PatientContactInfo(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

_patient_contact_info = PatientContactInfo

class PatientPersonalInfo(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None

_patient_personal_info = PatientPersonalInfo

class PatientAppointment(BaseModel):
    appointment_datetime: Optional[datetime] = None
    appointment_type: Optional[str] = None
    appointment_type_id: Optional[int] = None
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None
    doctor_specialization: Optional[str] = None
    doctor_specialization_id: Optional[int] = None
    appointment_status: Optional[str] = None
    appointment_status_id: Optional[int] = None

_patient_appointment = PatientAppointment

class PatientNote(BaseModel):
    note: Optional[str] = None
    note_id: Optional[int] = None
    subject: Optional[str] = None
    note_reason: Optional[str] = None
    note_reason_id: Optional[int] = None
    note_datetime: Optional[datetime] = None

_patient_note = PatientNote

class Patient(BaseModel):
    id: Optional[int] = None
    lastupdated: Optional[datetime] = None
    PatientPersonalInfo: Optional[_patient_personal_info] = None
    PatientContactInfo: Optional[_patient_contact_info] = None
    PatientAppointment: Optional[_patient_appointment] = None
    PatientNote: Optional[_patient_note] = None

class PatientLogin(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None