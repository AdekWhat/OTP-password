from django import forms
from django.forms import ModelForm
from .models import Users
from django.core.exceptions import ValidationError

class CheckPhoneForm(forms.Form):
    phone_number = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        # TODO: If will be enougt time add another checks for phone number field
        if not phone_number:
            raise ValidationError({ 'phone_number' : "Please, entry phone field"})
        return cleaned_data

class UserLoginForm(forms.Form):
    otp_field = forms.CharField(max_length = 4)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UserLoginForm, self).__init__(*args, **kwargs)

    def clean_otp_field(self):
        otp_field = self.cleaned_data.get('otp_field')
        if otp_field != self.request.session['OTP-pass']:
            raise ValidationError({ 'otp_field' : "Wrong OTP password"})
        return otp_field

class EmployeeLoginForm(UserLoginForm):
    password = forms.CharField()


class UserRegistrationForm(forms.Form):
    name = forms.CharField()
    otp_field = forms.CharField(max_length = 4)
    password = forms.CharField()

    # pass reques array in form constructor
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        password = cleaned_data.get('password')
        otp_field = cleaned_data.get('otp_field')
        # in case frontend validation will be off
        if not name or not password or not confirm_password or not otp_field:
            raise forms.ValidationError("All fields must be entered")

        # Just in case
        # if len(password) < 6:
        #     raise ValidationError({ 'password' : "Password too short"})

        if otp_field != self.request.session.get('OTP-pass', False):
            raise ValidationError({ 'otp_field' : "Wrong OTP password"})

        return cleaned_data


class AdminRegistrationForm(UserRegistrationForm):
    confirm_password  = forms.CharField()

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError({ 'confirm_password' : "Passwords must be equal"})
        return confirm_password
