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

WAKTU_PELAKSANAAN = (
    ('08:30 - 14:00 WIB', '08:30 - 14:00 WIB'),
    ('14:00 - 20:00 WIB', '14:00 - 20:00 WIB'),
    ('20:00 - 02:00 WIB', '20:00 - 02:00 WIB'),
    ('02:00 - 08:30 WIB', '02:00 - 08:30 WIB'),
)

def get_default_date():
    return timezone.now().astimezone(pytz.timezone('Asia/Jakarta')).date()

class BastRecordModel(models.Model):
    date = models.DateField(default=get_default_date)
    bast_id = models.CharField(max_length=17, default='0')
    waktu_pelaksanaan = models.CharField(choices=WAKTU_PELAKSANAAN, max_length=20, default='08:30 - 14:00 WIB', blank=True, null=True)
    shift = models.CharField(max_length=15, choices=SHIFT, default='Pagi')
    kelompok = models.CharField(max_length=1, choices=KELOMPOK, default='1')
    kel_berikut = models.CharField(max_length=1, choices=KELOMPOK, default='1')
    events = models.TextField(default='0')
    spv = models.ForeignKey(Operator, on_delete=models.CASCADE)
    NIP = models.CharField(max_length=18, default='0', blank=True)
    event_indonesia = models.IntegerField(default=0)
    event_luar = models.IntegerField(default=0)
    event_dirasakan = models.IntegerField(default=0)
    event_dikirim = models.IntegerField(default=0)
    member = models.TextField(max_length=1000, default='')
    count_gaps = models.IntegerField(default=0)
    count_spikes = models.IntegerField(default=0)
    count_blanks = models.IntegerField(default=0)
    waktu_cs = models.CharField(max_length=20, default='00:00 WIB', blank=True, null=True)
    pulsa_poco = models.IntegerField(default=0)
    poco_exp = models.DateField(default=get_default_date)
    pulsa_samsung = models.IntegerField(default=0)
    samsung_exp = models.DateField(default=get_default_date)
    notes = models.TextField(max_length=1000, default='', blank=True, null=True)

    def __str__(self):
        return self.bast_id
