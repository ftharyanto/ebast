from django.db import models
from django.utils import timezone
from core.models import Operator

# class CsRecordModel(models.Model):
#     # fields of the model
#     cs_id = models.CharField(max_length=15, default='0')
#     tanggal = models.DateField()
#     jam = models.CharField(max_length=20, choices=WAKTU, default='12:00 WIB')
#     kelompok = models.IntegerField(choices=KELOMPOK, default=1)
#     operator = models.TextField(null=True,)
#     gaps = models.TextField(max_length=3000, null=True, blank=True)
#     spikes = models.TextField(max_length=3000, null=True, blank=True)
#     blanks = models.TextField(max_length=3000, null=True, blank=True)
#     slmon = models.PositiveIntegerField(null=True, blank=True, default=0)
#     count_gaps = models.IntegerField(default=0, blank=True)
#     count_spikes = models.IntegerField(default=0, blank=True)
#     count_blanks = models.IntegerField(default=0, blank=True)

#     def save(self, *args, **kwargs):
#         seismograph_list = StationListModel.objects.values_list('kode', flat=True)

#         def remove_accelerograph(data):
#             for item in data:
#                 if item not in seismograph_list:
#                     data.remove(item)
#             return data
        
#         # Modify the group field here
#         if self.gaps:
#             self.gaps = self.gaps.upper()
#             self.gaps = remove_accelerograph(self.gaps.split('\r\n'))
#             self.count_gaps = len(self.gaps)

#         if self.spikes:
#             self.spikes = self.spikes.upper()
#             self.spikes = remove_accelerograph(self.spikes.split('\r\n'))
#             self.count_spikes = len(self.spikes)

#         if self.blanks:
#             self.blanks = self.blanks.upper()
#             self.blanks = remove_accelerograph(self.blanks.split('\r\n'))
#             self.count_blanks = len(self.blanks)

#         super().save(*args, **kwargs)
class CsRecord(models.Model):
    # KELOMPOK_CHOICES = [
    #     ('1', '1'),
    #     ('2', '2'),
    #     ('3', '3'),
    #     ('4', '4'),
    #     ('5', '5'),
    # ]
    # kelompok = models.CharField(max_length=1, choices=KELOMPOK_CHOICES, default='1')
    # jam_pelaksanaan = models.TimeField(default=(timezone.now() + timezone.timedelta(hours=7)).replace(second=0, microsecond=0))
    # qc_prev = models.TextField(default='0')
    # qc = models.TextField(default='0')
    # operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    # NIP = models.CharField(max_length=18, default='0')
    # event_indonesia = models.IntegerField(default=0)
    # event_luar = models.IntegerField(default=0)

    def __str__(self):
        return self.cs_id

class StationListModel(models.Model):
    network = models.CharField(max_length=5)
    code = models.CharField(max_length=10)
    province = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    digitizer_type = models.CharField(max_length=100)
    UPT = models.CharField(max_length=50)

    def __str__(self):
        return self.code