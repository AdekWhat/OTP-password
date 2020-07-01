from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from .forms import CheckPhoneForm, AdminRegistrationForm, UserRegistrationForm, UserLoginForm, EmployeeLoginForm
from django.http import HttpResponse,HttpResponseRedirect
from .models import Users, Departmens
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
# for OTP generation
from random import choice
from string import ascii_letters, digits


class CheckPhoneView(FormView):
    template_name = 'index.html'
    form_class = CheckPhoneForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        logout(request)
        return render(request, self.template_name, { 'form': form })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # creating OTP pass with 4 symbols lenght
            otp = self.OTPGeneration(4)
            #Saving OTP var in session
            request.session['OTP-pass'] = otp
            #
            user_phone = form.cleaned_data.get('phone_number')
            request.session['user_phone'] = user_phone
            query = Users.objects.all()
            if len(query) == 0:
                return HttpResponseRedirect('admin_registration/')  # Redirect to admin registration page
            elif not query.filter(phone_number = user_phone):
                return HttpResponseRedirect('user_registation/') # Redirect to user reg page
            elif query.filter(phone_number = user_phone).filter(is_employee = True):
                return HttpResponseRedirect('employee_login/') # redirect to login user page
            elif query.filter(phone_number = user_phone):
                return HttpResponseRedirect('user_login/') # redirect not dep. user login page
            else:
                return HttpResponse('Opps, something goes wrong',status=500)


    def OTPGeneration(self, size):
            otp = ''.join(choice(ascii_letters + digits) for _ in range(size))
            print(otp)
            return otp

class UserRegistrationView(FormView):
    template_name = 'index.html'
    form_class = UserRegistrationForm

    def get_form_kwargs(self):
         kwargs = super().get_form_kwargs()
         kwargs['request'] = self.request
         return kwargs

    def get(self, request, *args, **kwargs):
        if not request.session.get('user_phone', False):
             return HttpResponseRedirect('/')

        form = self.form_class(request = request)
        return render(request, self.template_name, { 'form': form })

    def form_valid(self, form):
        admin_user = Users()
        admin_user.name = form.cleaned_data.get('name')
        admin_user.set_password(form.cleaned_data.get('password'))
        # print(admin_user.set_password(form.cleaned_data.get('password'))) # Need research this bug
        admin_user.phone_number = self.request.session.get('user_phone') # TODO: need to check is it possible situation when on get - session store phone number, but in post it haven't it
        admin_user.status = True
        admin_user.is_employee = False
        admin_user.departmen = Departmens.objects.get(pk = 1)
        admin_user.save()
        login(self.request, admin_user) # It neaded
        return HttpResponseRedirect('/hello/')

class AdminRegistrationView(UserRegistrationView):
    template_name = 'index.html'
    form_class = AdminRegistrationForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('user_phone', False) or Users.objects.all().exists(): #TODO: Need 'explain' db query
             return HttpResponseRedirect('/')

        form = self.form_class(request = request)
        return render(request, self.template_name, { 'form': form })

    def form_valid(self, form):
        admin_user = Users()
        admin_user.name = form.cleaned_data.get('name')
        admin_user.set_password(form.cleaned_data.get('password'))
        # print(admin_user.set_password(form.cleaned_data.get('password'))) #TODO: Need research this bug
        admin_user.phone_number = self.request.session.get('user_phone') # TODO: need to check is it possible situation when on get - session store phone number, but in post it haven't it
        admin_user.status = True
        admin_user.is_employee = True
        admin_user.departmen = Departmens.objects.get(pk = 1)
        admin_user.save()
        login(self.request, admin_user) # It neaded
        return HttpResponseRedirect('/hello/')

class UserLoginView(FormView):
    template_name = 'index.html'
    form_class = UserLoginForm
    success_url = '/hello/'

    def get(self, request, *args, **kwargs):
        if not request.session.get('user_phone', False):
            return HttpResponseRedirect('/')

        form = self.form_class(request = request)
        return render(request, self.template_name, { 'form': form })

    def get_form_kwargs(self):
         kwargs = super().get_form_kwargs()
         kwargs['request'] = self.request
         return kwargs


class EmployeeLoginView(UserLoginView):
    form_class = EmployeeLoginForm

    def form_valid(self, form):
        user = Users.objects.get(phone_number = self.request.session.get('user_phone'))
        if not user.check_password(form.cleaned_data.get('password')):
            return render(self.request, 'wrong_pass.html')
        return HttpResponseRedirect('/hello/')

class HelloPageView(View):
    template_name = 'hello.html'

    def get(self, request, *args, **kwargs):
        try:
            user = Users.objects.get(phone_number = request.session.get('user_phone'))
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'user': user})
