from django.contrib import admin

# Register your models here.
from .models import Departmens, Users

admin.site.register(Departmens)
admin.site.register(Users)
