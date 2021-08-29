from django.shortcuts import render
from django.views.generic import CreateView

from ahms.appointments.forms import PatientApplications
from ahms.appointments.models import Appointment


# class PatientAppointmentView(CreateView):
#     # model = Appointment
#     form_class = PatientApplications
#     template_name = 'users/patient_appointment_form.html'

# def get_context_data(self, **kwargs):
#     kwargs['user_type'] = 'patient'
#     return super().get_context_data(**kwargs)
#
# def form_valid(self, form):
#     print(form)
#     user = form.save()
#     login(self.request, user)
#     return redirect('home')


# There should be a dashboard were every patient can see their checkins
# and checkout off the hospital.
def main_dashboard(request):
    pass


def patient_history_dashboard(request):
    pass


def appointment(request):
    applicant_form = PatientApplications()
    return render(request, "index.html", {'applicant_form': applicant_form})
