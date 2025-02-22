from django.db import models
from django.utils import timezone
from core.models import Operator
import pytz

KELOMPOK = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

SHIFT = (
    ('Pagi', 'Pagi'),
    ('Siang', 'Siang'),
    ('Malam', 'Malam'),
    ('Dini Hari', 'Dini Hari'),
)

def get_default_date():
    return timezone.now().astimezone(pytz.timezone('Asia/Jakarta')).date()

class BastRecordModel(models.Model):
    date = models.DateField(default=get_default_date)
    bast_id = models.CharField(max_length=17, default='0')

    shift = models.CharField(max_length=15, choices=SHIFT, default='Pagi')
    kelompok = models.CharField(max_length=1, choices=KELOMPOK, default='1')
    kel_berikut = models.CharField(max_length=1, choices=KELOMPOK, default='1')
    events = models.TextField(default='0')
    spv = models.ForeignKey(Operator, on_delete=models.CASCADE)
    NIP = models.CharField(max_length=18, default='0')
    event_indonesia = models.IntegerField(default=0)
    event_luar = models.IntegerField(default=0)
    event_dirasakan = models.IntegerField(default=0)
    event_dikirim = models.IntegerField(default=0)
    member = models.CharField(max_length=300, default='')

    def __str__(self):
        return self.bast_id
