from allauth.account.views import login
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView

# from ahms.appointments.models import Appointment
from ahms.users.forms import PatientSignUpForm, NurseSignUpForm, DoctorSignUpForm
from ahms.users.models import Patient, Nurse, Doctor

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


## Patient SignUp View ##
class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'users/patient_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # print(form)
        user = form.save()
        print(form.cleaned_data)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user1 = authenticate(
            username=username,
            password=password)
        print(user1.is_anonymous)
        if user1.is_active:
            login(self.request, user1)
        return redirect('patient_profile_update')


class PatientProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Patient
    fields = ["profile_pic", "address", "mobile"]
    template_name = "pages/patient-profile.html"
    success_message = _("Information successfully updated")

    # success_url = reverse_lazy('patient_detail')

    def get_object(self):
        return self.request.user

    # def form_valid(self, form):
    #     p_update = form.save(commit=False)
    #     p_update.updated_by = self.request.user
    #     p_update.save()
    #     return redirect('patient_detail')


# class PatientDetail(LoginRequiredMixin, DetailView):
#     template_name = "users/patient.html"
#
#     def get_object(self):
#         return self.request.user


## Nurse SignUp View ##

class NurseSignUpView(CreateView):
    model = User
    form_class = NurseSignUpForm
    template_name = 'users/nurse_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'nurse'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('nurse:check_patient')


class NurseProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Nurse
    fields = ["profile_pic", "address", "mobile", "role", ]
    template_name = "pages/patient-profile.html"
    success_message = _("Information successfully updated")

    # success_url = reverse_lazy('patient_detail')

    def get_object(self):
        return self.request.user

    # def form_valid(self, form):
    #     p_update = form.save(commit=False)
    #     p_update.updated_by = self.request.user
    #     p_update.save()
    #     return redirect('patient_detail')


## Doctor SignUp View ##

class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'users/doctor_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # print(form)
        user = form.save()
        print(form.cleaned_data)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user1 = authenticate(
            username=username,
            password=password)
        print(user1.is_anonymous)
        if user1.is_active:
            login(self.request, user1)
        return redirect('home')


class DoctorProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Doctor
    fields = ["profile_pic", "address", "mobile", "department", "role"]
    template_name = "pages/patient-profile.html"
    success_message = _("Information successfully updated")

    # success_url = reverse_lazy('patient_detail')

    def get_object(self):
        return self.request.user

    # def form_valid(self, form):
    #     p_update = form.save(commit=False)
    #     p_update.updated_by = self.request.user
    #     p_update.save()
    #     return redirect('patient_detail')


def home(request):
    if request.user.is_authenticated:
        if request.user.is_nurse:
            print("user migth be patient")
            # appointment = Appointment.objects.count()
            # patients = Patient.objects.count()
            return render(request, template_name="pages/admin-index.html", context={'hello': "hello"})
    print("user isn't doctor or nurse")
    print(request.user.is_nurse)
    return render(request, template_name="pages/admin-index.html", context={'hello': "hello"})
