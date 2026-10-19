# bookings/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Service(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_CONFIRMED = 'CONFIRMED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    scheduled_at = models.DateTimeField()
    phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_at']
        constraints = [
            models.UniqueConstraint(fields=['service', 'scheduled_at'], name='unique_service_datetime')
        ]

    def __str__(self):
        return f"{self.service.name} – {self.user} at {self.scheduled_at:%Y-%m-%d %H:%M}"
