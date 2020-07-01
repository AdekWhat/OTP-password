from django.urls import  path, re_path
# from . import views
from .views import CheckPhoneView, AdminRegistrationView, HelloPageView, UserRegistrationView, UserLoginView, EmployeeLoginView
from django.contrib.auth.decorators import login_required

urlpatterns = [

    re_path('^$', CheckPhoneView.as_view(), name = "index"),
    path('admin_registration/', AdminRegistrationView.as_view(), name = 'admin_registration'),
    path('user_registation/', UserRegistrationView.as_view(), name = 'user_registation'),
    path('employee_login/', EmployeeLoginView.as_view(), name = 'employee_login'),
    path('user_login/', UserLoginView.as_view(), name = 'user_login'),
    path('hello/', HelloPageView.as_view(), name = 'hello')

]
