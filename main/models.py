from django.db import models

# Create your models here.

class Departmens(models.Model):
    name = models.CharField(max_length = 100)
    department_code = models.CharField(max_length = 6)

class Users(models.Model):
    name = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 13)
    status = models.BooleanField()
    is_employee = models.BooleanField() # # TODO: Проиндексировать когда ставится значение тру
    departmen = models.ForeignKey('Departmens', on_delete = models.CASCADE)
