from django.db import models
from core.models import Operator
from PIL import Image  # Add this import

KELOMPOK = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

WAKTU = (
    ('00:00 WIB', '00:00 WIB'),
    ('06:00 WIB', '06:00 WIB'),
    ('12:00 WIB', '12:00 WIB'),
    ('18:00 WIB', '18:00 WIB'),
)

SHIFT = (
    ('Pagi', 'Pagi'),
    ('Siang', 'Siang'),
    ('Malam', 'Malam'),
    ('Dini Hari', 'Dini Hari'),
)

class CsRecordModel(models.Model):
    # fields of the model
    cs_id = models.CharField(max_length=15, default='0')
    shift = models.CharField(max_length=15, choices=SHIFT, default='P')
    jam_pelaksanaan = models.CharField(max_length=20, choices=WAKTU, default='12:00 WIB')
    kelompok = models.IntegerField(choices=KELOMPOK, default=1)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    gaps = models.TextField(max_length=10000, null=True, blank=True)
    spikes = models.TextField(max_length=10000, null=True, blank=True)
    blanks = models.TextField(max_length=10000, null=True, blank=True)
    slmon = models.PositiveIntegerField(null=True, blank=True, default=0)
    count_gaps = models.PositiveIntegerField(null=True, blank=True, default=0)
    count_spikes = models.PositiveIntegerField(null=True, blank=True, default=0)
    count_blanks = models.PositiveIntegerField(null=True, blank=True, default=0)
    slmon_image = models.ImageField(upload_to='cl_seiscomp/slmon_images/', null=True, blank=True)

    def __str__(self):
        return self.cs_id

    def save(self, *args, **kwargs):
        sensor_list = StationListModel.objects.values_list('code', flat=True)

        def clean_sensor(data):
            for item in data:
                if item not in sensor_list:
                    data.remove(item)
            return data
        
        # Modify the group field here
        if self.gaps:
            self.gaps = self.gaps.upper()
            self.gaps = clean_sensor(self.gaps.splitlines())
            self.count_gaps = len(self.gaps)
            self.gaps = '\n'.join(self.gaps)

        if self.spikes:
            self.spikes = self.spikes.upper()
            self.spikes = clean_sensor(self.spikes.splitlines())
            self.count_spikes = len(self.spikes)
            self.spikes = '\n'.join(self.spikes)

        if self.blanks:
            self.blanks = self.blanks.upper()
            self.blanks = clean_sensor(self.blanks.splitlines())
            self.count_blanks = len(self.blanks)
            self.blanks = '\n'.join(self.blanks)

        super().save(*args, **kwargs)
        if self.slmon_image:
            img = Image.open(self.slmon_image.path) # Open slmon_image using self

            if img.height > 1006 or img.width > 600:
                new_img = (1006, 600)
                img.thumbnail(new_img)
                img.save(self.slmon_image.path)
            
class StationListModel(models.Model):
    network = models.CharField(max_length=5)
    code = models.CharField(max_length=10)
    province = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    digitizer_type = models.CharField(max_length=100)
    UPT = models.CharField(max_length=50)

    def __str__(self):
        return self.code