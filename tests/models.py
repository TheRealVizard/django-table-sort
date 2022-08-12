from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    age = models.IntegerField(verbose_name="Age in years")
