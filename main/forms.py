from django import forms

class CheckPhoneForm(forms.Form):
    phone_number = forms.CharField()


    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
