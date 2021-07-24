from django import forms

from ahms.appointments.models import Appointment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('text', )
