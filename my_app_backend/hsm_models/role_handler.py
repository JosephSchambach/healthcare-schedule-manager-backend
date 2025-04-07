import hsm_models.admin as admin
import hsm_models.doctor as doctor
import hsm_models.patient as patient

def get_user_role(role: str, username: str, password: str):
    if role == "admin": 
        return admin.AdministratorLogin(username=username, password=password)
    elif role == "doctor":
        return doctor.DoctorLogin(username=username, password=password)
    elif role == "patient":
        return patient.PatientLogin(username=username, password=password)