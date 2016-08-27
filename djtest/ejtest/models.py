from django.db import models

# Create your models here.

class Model1(models.Model):
    charattr = models.CharField(max_length=10)
    intattr = models.IntegerField()

class Model2(models.Model):
    charattr = models.CharField(max_length=10)
    model1 = models.ForeignKey(Model1)

