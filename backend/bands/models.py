from django.db import models
from django.conf import settings


class Band(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_band')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BandMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='band_memberships'
    )
    band = models.ForeignKey(
        Band,
        on_delete=models.CASCADE,
        related_name='bands'
    )

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='member')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'band')
        ordering = ['band', 'role']

    def __str__(self):
        return f"{self.user.username} - {self.band.name} ({self.role})"
