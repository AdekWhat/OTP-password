from django.shortcuts import render

# Create your views here.
# from myapp.forms import ContactForm
from django.views.generic.edit import FormView
from .forms import CheckPhoneForm

class CheckPhoneView(FormView):
    template_name = 'index.html'
    form_class = CheckPhoneForm
    # success_url = '/thanks/'

    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     # form.send_email()
    #     return super(ContactView, self).form_valid(form)
