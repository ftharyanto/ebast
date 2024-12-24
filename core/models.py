from django.db import models

# Create your models here.
class Operator(models.Model):
    name = models.CharField(max_length=100)
    NIP = models.CharField(max_length=18)

    def __str__(self):
        return self.name
