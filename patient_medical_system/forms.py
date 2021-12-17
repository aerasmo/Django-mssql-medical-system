from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
class UserForm(forms.ModelForm):
    re_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields = ['first_name','last_name','username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput()
        }
    def clean(self):
        self.cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('Password Does not Match')
        return self.cleaned_data


class PatientForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = ['profile_pic', 'phone_number', 'age', 'sex']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = [
            'appointment_type'
        ]
class MedicalInformationForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = [
            'weight', 
            'height', 
            'sex', 
            'has_glasses', 
            'blood_type', 
            'vision_level', 
            'eye_condition', 
            'has_glasses',
            'notes'
        ]

class DischargeForm(forms.ModelForm):
    class Meta:
        model = models.Discharge
        fields = [
            'consultation_fee',
            'room_fee',
            'medicine_fees',
            'other_fees'
        ]