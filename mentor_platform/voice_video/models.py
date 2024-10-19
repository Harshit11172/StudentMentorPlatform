from django.db import models
from users.models import Mentor, Mentee  # Adjust based on your actual user models

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
        ('issue raised', 'Issue Raised'),
        ('issue resolved', 'Issue Resolved'), 
    ]
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    channel_name = models.CharField(max_length=255, blank=True)  # Will store generated channel name
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created
    booking_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Booking amount in currency")  # New field for booking amount
    
    def __str__(self):
        return f"{self.mentee.user.username} with {self.mentor.user.username} on {self.scheduled_time}"
