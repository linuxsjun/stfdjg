from django.test import TestCase

# Create your tests here.

from django.db import models

class hr_Test(models.Model):
    name=models.CharField(max_length=32)
    crnu=models.IntegerField(default=1)

    class Meta:
        db_table='hr_test'