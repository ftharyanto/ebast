from django.db import models
from django.utils import timezone
from core.models import Operator

class QcRecord(models.Model):
    qc_id = models.CharField(max_length=15, default='0')
    KELOMPOK_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    kelompok = models.CharField(max_length=1, choices=KELOMPOK_CHOICES, default='1')
    jam_pelaksanaan = models.TimeField(default=(timezone.now() + timezone.timedelta(hours=7)).replace(second=0, microsecond=0))
    qc_prev = models.TextField(default='0')
    qc = models.TextField(default='0')
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    NIP = models.CharField(max_length=18, default='0')
    event_indonesia = models.IntegerField(default=0)
    event_luar = models.IntegerField(default=0)
    kel_sebelum = models.CharField(max_length=1, choices=KELOMPOK_CHOICES, default='1')

    def __str__(self):
        return self.qc_id
