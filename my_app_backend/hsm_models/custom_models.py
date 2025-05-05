import my_app_backend.hsm_appointment_manager.appointment_scheduler as appt_sched
import my_app_backend.hsm_auth.registrar as reg
import my_app_backend.hsm_models.patient as pat
import my_app_backend.hsm_models.doctor as doc
import my_app_backend.hsm_models.admin as adm

def get_obj_config():
    data = {
        "CreatePatientAppointment": {
            "parent_method": appt_sched.AppointmentScheduler.schedule,
            "kwargs": {
                "attribute": "appointment",
                "context_method": "database",
                "execution_method": "insert"
            }
        },
        "CreatePatient": {
            "parent_method": reg.Registrar.register,
            "kwargs": {
                "registrar": pat.Patient
            }
        },
        "UpdatePatientAppointment": {
            "parent_method": appt_sched.AppointmentScheduler.reschedule,
            "kwargs": {
                "attribute": "condition",
                "update_data": "values_to_update",
                "context_method": "database",
                "execution_method": "update"
            }
        },
        "DeletePatientAppointment": {
            "parent_method": appt_sched.AppointmentScheduler.cancel,
            "kwargs": {
                "attribute": "condition",
                "context_method": "database",
                "execution_method": "delete"
            }
        }
    }
    return data