from typing import Optional, Literal, Dict, List
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

class PatientPersonalInfo(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None

class PatientAppointment(BaseModel):
    appointment_id: Optional[str] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    appointment_type: Optional[str] = None
    appointment_type_id: Optional[int] = None
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None
    appointment_status: Optional[str] = None
    appointment_status_id: Optional[int] = None
    notes: Optional[str] = None
    patient_name: Optional[str] = None
    patient_id: Optional[int] = None

class PatientNote(BaseModel):
    note: Optional[str] = None
    note_id: Optional[int] = None
    subject: Optional[str] = None
    note_reason: Optional[str] = None
    note_reason_id: Optional[int] = None
    note_datetime: Optional[datetime] = None

class Patient(BaseModel):
    id: Optional[int] = None
    lastupdated: Optional[datetime] = None
    personal_info: Optional[PatientPersonalInfo] = None
    contact_info: Optional[PatientContactInfo] = None
    appointment: Optional[PatientAppointment] = None
    note: Optional[PatientNote] = None

class PatientLogin(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = "patient"

class CreatePatientAppointment(BaseModel):
    appointment: Optional[PatientAppointment] = None
    
class UpdatePatientAppointment(BaseModel):
    condition: Optional[Dict] = None
    values_to_update: Optional[Dict] = None
    
class DeletePatientAppointment(BaseModel):
    condition: Optional[Dict] = None
    
class GetPatientAppointments(BaseModel):
    columns: Optional[List] = None
    condition: Optional[Dict] = None