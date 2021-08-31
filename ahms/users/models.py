from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, OneToOneField
from django.db.models.enums import TextChoices
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Awesome Hostel Management System."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
    
    def __str__(self):
        return f"{self.name}"


## Patient ##

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='patient')
    profile_pic = models.ImageField(
        upload_to="profile_pic/PatientProfilePic/", null=True, blank=True
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    # symptoms = models.CharField(max_length=100, null=False)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f"{self.user.name}"


## Nurse ##

class Nurse(models.Model):
    class NurseRoles(TextChoices):
        NURSE_UNIT_MANAGER = "NURSE UNIT MANAGER", "Nurse Unit Manager"
        ASSOCIATE_NURSE_UNIT_MANAGER = (
            "ASSOCIATE NURSE UNIT MANAGER",
            "Associate Nurse Unit Manager",
        )
        NURSE_PRACTITIONER = "NURSE PRACTITIONER", "Nurse Practitioners"
        REGISTERED_NURSES = "REGISTERED NURSES", "Registered Nurses"
        ENROLLED_NURSES = "ENROLLED NURSES" "Enrolled Nurses"

    user = OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/NurseProfilePic/", null=True, blank=True
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    # department = models.CharField(max_length=50, choices=departments, default='Cardiologist')
    role = CharField(
        _("Role"),
        max_length=50,
        choices=NurseRoles.choices,
        default=NurseRoles.ENROLLED_NURSES,
    )
    # role = models.CharField(max_length=50, choices=roles, default='null')
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f"{self.user.name}"

        # return self.user.first_name + " is a" + " (" + self.role + ")"


## Doctor Models ##
departments = [
    ("Cardiologist", "Cardiologist"),
    ("Dermatologists", "Dermatologists"),
    ("Emergency Medicine Specialists", "Emergency Medicine Specialists"),
    ("Allergists/Immunologists", "Allergists/Immunologists"),
    ("Anesthesiologists", "Anesthesiologists"),
    ("Colon and Rectal Surgeons", "Colon and Rectal Surgeons"),
]

class Doctor(models.Model):
    class Roles(TextChoices):
        SENIOR_CONSULTANT = "SENIOR CONSULTANT", "Senior Consultant"
        REGISTRARS = "REGISTRAR", "Registrars"
        RESIDENTS = "RESIDENT", "Residents"
        INTERNS = "INTERN", "Interns"
        STUDENT_DOCTOR = "STUDENT DOCTOR" "Student Doctor"

    user = OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/DoctorProfilePic/", null=True, blank=True
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(
        max_length=50, choices=departments, default="Cardiologist"
    )
    role = CharField(
        _("Type"), max_length=50, choices=Roles.choices, default=Roles.INTERNS
    )
    # role = models.CharField(max_length=50, choices=roles, default='null')
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f"{self.user} - A/An {self.role} in {self.department} department"
