from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField  # If using PostgreSQL
from django.core.exceptions import ValidationError
import re


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)  # Ensure email is unique
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)
    # , default='mentee'
    verification_token = models.CharField(max_length=32, null=True, blank=True)  # Token for verification
    is_verified = models.BooleanField(default=False)  # Status to track email verification

    # Set custom related names to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users_user_set',  # Change this to avoid conflicts
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users_user_permissions',  # Change this to avoid conflicts
        blank=True,
    )

    def __str__(self):
        return self.username


class Mentor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='mentor_profile')
    phone_number = models.CharField(max_length=15, blank=True)  # Optional
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Academic Information
    university = models.CharField(max_length=255, blank=True)    #######
    degree = models.CharField(max_length=100, blank=True)  #######
    major = models.CharField(max_length=100, blank=True)    ########
    year_of_admission = models.IntegerField(null=True, blank=True)   ########
    college_id = models.CharField(max_length=100, blank=True)  # Optional

    # Mentorship Information
    expertise = models.CharField(max_length=255, blank=True)  # Optional

    available_days = models.JSONField(default=list, blank=True)  # Store days as a list
    # Sample input for available_days["Monday", "Tuesday", "Wednesday"]

    available_hours = JSONField(default=list, blank=True)  # Store time slots as a list
    # Sample input for available_hours["10am-11am", "1pm-2pm", "12pm-1am"]

    
    # session_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional   ######
    
    session_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=200.00
    )  # Default set to 200 INR
    
    rating = models.FloatField(default=0.0)

    # Entrance Exam Info
    entrance_exam_given = models.CharField(max_length=100, blank=True)  # Optional
    rank = models.IntegerField(null=True, blank=True)  # Optional
    score = models.FloatField(null=True, blank=True)  # Optional

    def clean(self):
        # Custom validation for available days
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if self.available_days:
            for day in self.available_days:
                if day not in valid_days:
                    raise ValidationError(f"Invalid day: {day}. Each day must be one of {', '.join(valid_days)}.")
        else:
            self.available_days = []

        # Custom validation for available hours
        if self.available_hours:
            for slot in self.available_hours:
                if not re.match(r"^\d{1,2}(am|pm)-\d{1,2}(am|pm)$", slot):
                    raise ValidationError("Each time slot must be in the format '10am-11am'.")
        else:
            self.available_hours = []
        # Custom validation to ensure session_fee is at least 200
        if self.session_fee is not None and self.session_fee < 200:
            raise ValidationError("Session fee must be at least 200 INR.")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.username}"

    class Meta:
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"


class Mentee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='mentee_profile')
    phone_number = models.CharField(max_length=15, blank=True)  # Optional
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Academic Information
    university = models.CharField(max_length=255, blank=True)  # Optional
    degree = models.CharField(max_length=100, blank=True)  # Optional
    major = models.CharField(max_length=100, blank=True)  # Optional
    year_of_study = models.IntegerField(null=True, blank=True)  # Optional
    college_id = models.CharField(max_length=100, blank=True)  # Optional

    # Mentorship Preferences
    desired_expertise = models.CharField(max_length=255, blank=True)  # Optional
    preferred_session_times = models.TextField(blank=True)  # Optional
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional

    # Additional Information
    goals = models.TextField(blank=True)  # Optional
    feedback = models.TextField(blank=True)  # Optional

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.university}"

    class Meta:
        verbose_name = "Mentee"
        verbose_name_plural = "Mentees"


class Feedback(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE, related_name='feedbacks')  # Change 'feedback' to 'feedbacks'
    session_date = models.DateTimeField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"Feedback from {self.mentee.user.username} for {self.mentor.user.username} on {self.session_date}"



class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use CustomUser instead of User
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP {self.code} for {self.user.username}"

