from django.db import models
from django.urls import reverse
from django.utils import timezone

class PapanKlip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=1))

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Papan Klip'
        verbose_name_plural = 'Papan Klip'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('papan_klip:papan_klip_detail', kwargs={'pk': self.pk})
