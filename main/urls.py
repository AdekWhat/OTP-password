from django.urls import  path, re_path
# from . import views
from .views import CheckPhoneView
from django.contrib.auth.decorators import login_required

urlpatterns = [

    re_path('^$', CheckPhoneView.as_view(), name = "index"),

]
