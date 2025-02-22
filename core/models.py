from django.db import models

# Create your models here.
class Operator(models.Model):
    name = models.CharField(max_length=100)
    NIP = models.CharField(max_length=18)
    nickname = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

class Kelompok(models.Model):
    KELOMPOK_CHOICES = models.IntegerChoices('Kelompok', '1 2 3 4 5 6')
    name = models.IntegerField(choices=KELOMPOK_CHOICES.choices, default=1)
    member = models.ManyToManyField(Operator)

    def __str__(self):
        return str(self.name)