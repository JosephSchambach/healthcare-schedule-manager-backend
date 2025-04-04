from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class AdministratorPersonalInfo(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    role_id: Optional[int] = None
    years_of_experience: Optional[int] = None

_admin_personal_info = AdministratorPersonalInfo

class AdministratorContactInfo(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

_admin_contact_info = AdministratorContactInfo

class Administrator(BaseModel):
    id: Optional[int] = None
    AdministratorPersonalInfo: Optional[_admin_personal_info] = None
    AdministratorContactInfo: Optional[_admin_contact_info] = None

class AdministratorLogin(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None