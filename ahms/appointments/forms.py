from django import forms
from django.forms.models import ModelForm

from ahms.appointments.models import Appointment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('text', )


class PatientApplications(ModelForm):

    class Meta:
        model = Appointment
        fields = ['description', ]
