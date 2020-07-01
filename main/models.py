from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class Departmens(models.Model):
    name = models.CharField(max_length = 100)
    department_code = models.CharField(max_length = 6)

    def __str__(self):
        return self.name

class Users(AbstractBaseUser):
    name = models.CharField(max_length = 50)
    password = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 13, db_index = True, unique = True)
    status = models.BooleanField()
    is_employee = models.BooleanField() 
    department = models.ForeignKey('Departmens', null = True, on_delete = models.SET_NULL)


    def __str__(self):
        return self.name
