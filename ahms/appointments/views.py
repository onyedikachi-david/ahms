from django.shortcuts import render
from django.views.generic import CreateView

class PatientAppointmentView(CreatView):
    model = Appointment
    form_class = PatientSignUpForm
    template_name = 'users/patient_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        print(form)
        user = form.save()
        login(self.request, user)
        return redirect('home')
