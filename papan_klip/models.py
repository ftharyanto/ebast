import os
import os
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save

def upload_to(instance, filename):
    """
    Returns a unique filename for the uploaded file while preserving the original filename's case.
    The filename will be in the format: papan_klip/original_name_uuid.ext
    """
    import uuid
    
    # Get the file extension and base name
    base, ext = os.path.splitext(filename)
    
    # Generate a UUID and keep only the first 8 characters
    unique_id = str(uuid.uuid4())[:8]
    
    # Keep the original filename and append the UUID
    # Replace any problematic characters with underscores
    safe_base = base.replace(' ', '_')
    
    # Return the new filename with path, preserving the original case
    return f'papan_klip/{safe_base}_{unique_id}{ext}'

class PapanKlip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=upload_to, blank=True, null=True, verbose_name='Attached File')
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

    def delete(self, *args, **kwargs):
        """
        Override delete() to ensure the file is deleted when the model instance is deleted.
        """
        if self.file:
            # Delete the file from storage
            storage, path = self.file.storage, self.file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


@receiver(pre_delete, sender=PapanKlip)
def delete_file_on_model_delete(sender, instance, **kwargs):
    """
    Signal receiver to delete the file when the model instance is deleted.
    This is a backup in case delete() is not called directly.
    """
    if instance.file:
        instance.file.delete(save=False)


@receiver(pre_save, sender=PapanKlip)
def delete_old_file_on_update(sender, instance, **kwargs):
    """
    Delete old file when updating the file field.
    """
    if not instance.pk:
        return  # New instance, no file to delete

    try:
        old_instance = PapanKlip.objects.get(pk=instance.pk)
    except PapanKlip.DoesNotExist:
        return  # Instance doesn't exist yet

    # Check if the file has changed
    if old_instance.file and old_instance.file != instance.file:
        old_instance.file.delete(save=False)
