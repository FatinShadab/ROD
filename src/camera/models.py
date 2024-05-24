from django.db import models
from django.contrib.auth.models import User

class Camera(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cameras')
    cname = models.CharField(max_length=255, null=False, blank=False, unique=True)  # Name of the camera
    cip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=False, blank=False)  # IP address of the camera
    cport = models.PositiveIntegerField(null=False, blank=False)  # Port number
    selected = models.BooleanField(default=False)  # If selected, others should be false

    def serialize(self):
        return {
            'name': self.cname,
            'ip': self.cip,
            'cport': self.cport,
        }

    def get_url(self):
        return f"https://{self.cip}:{self.cport}"

    def save(self, *args, **kwargs):
        if self.selected:
            # Ensure only one camera is selected per user
            Camera.objects.filter(user=self.user, selected=True).update(selected=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cname} ({self.cip}:{self.cport}) - {'Selected' if self.selected else 'Not Selected'}"
