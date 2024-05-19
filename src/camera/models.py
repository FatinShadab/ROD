from django.db import models
from django.contrib.auth.models import User

class Camera(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cameras')
    cname = models.CharField(max_length=255)  # Name of the camera
    cip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)  # IP address of the camera
    cport = models.PositiveIntegerField()  # Port number
    selected = models.BooleanField(default=False)  # If selected, others should be false

    def save(self, *args, **kwargs):
        if self.selected:
            # Ensure only one camera is selected per user
            Camera.objects.filter(user=self.user, selected=True).update(selected=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cname} ({self.cip}:{self.cport}) - {'Selected' if self.selected else 'Not Selected'}"
