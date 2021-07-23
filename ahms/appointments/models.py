from django.db import models

from ahms.users.models import Patient, Doctor, Nurse


class AdmittedPatient(models.Model):
    patient_admitted = models.OneToOneField(Patient, on_delete=models.CASCADE)
    admitDate = models.DateField(auto_now=True)


## Appointment ##

class Appointment(models.Model):
    patient_appointment = models.OneToOneField(Patient, on_delete=models.CASCADE)
    doctor_assigned = models.OneToOneField(
        Doctor, on_delete=models.CASCADE, related_name="doctor_appointed"
    )
    nurse_assigned = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='nurse_assigned')
    first_time = models.BooleanField(verbose_name="Is it a first time appointment or not?", default=True)
    appointment_date = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)


## Patient Status ##

class PatientStatus(models.Model):
    patient_status = models.OneToOneField(Patient, on_delete=models.CASCADE)
    condition_choice = [
        ("Normal", "Normal"),
        ("Stable", "Stable"),
        ("Critical", "Critical"),
        ("Pending", "Pending"),
    ]
    condition = models.CharField(
        verbose_name="Patient Status/Condition",
        choices=condition_choice,
        default="Normal", max_length=20)
    added = models.DateTimeField(auto_created=True)

class Drugs(models.Model):
    name = models.CharField(verbose_name="Medication name", max_length=30)
    dose = models.CharField(verbose_name="Dosage", max_length=50)
    extra_info = models.CharField(verbose_name="Additional Information", max_length=250)
    side_effect = models.CharField(verbose_name="Any side effects", max_length=1000)


class Prescription(models.Model):
    patient_prescription = models.OneToOneField(Patient,
                                                on_delete=models.CASCADE,
                                                related_name="patient_prescription",
                                                )
    drugs = models.ForeignKey(Drugs,
                              verbose_name="Drug prescriptions",
                              related_name="patient_medications",
                              on_delete=models.CASCADE)
    doctor = models.OneToOneField(Doctor, verbose_name="Doctor Prescribing the drug",
                                  related_name="doctor_prescription", on_delete=models.CASCADE)
