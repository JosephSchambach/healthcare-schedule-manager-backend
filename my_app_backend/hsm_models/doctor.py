from typing import Optional
from pydantic import BaseModel, EmailStr

class DoctorContactInfo(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

_doctor_contact_info = DoctorContactInfo

class DoctorPersonalInfo(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    years_of_experience: Optional[int] = None
    specialization: Optional[str] = None
    specialization_id: Optional[int] = None

_doctor_personal_info = DoctorPersonalInfo

class Doctor(BaseModel):
    id: Optional[int] = None
    DoctorPersonalInfo: Optional[_doctor_personal_info] = None
    DoctorContactInfo: Optional[_doctor_contact_info] = None

class DoctorLogin(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None