from django.db import models
from django.utils import timezone
from django.conf import settings

class StoolRecord(models.Model):
    # Foreign key to the user model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stool_records'
    )
    STOOL_TYPES = [
        ('type1', 'Type 1 - Separate hard lumps'),
        ('type2', 'Type 2 - Sausage-shaped but lumpy'),
        ('type3', 'Type 3 - Sausage-shaped with cracks'),
        ('type4', 'Type 4 - Smooth and soft'),
        ('type5', 'Type 5 - Soft blobs with clear-cut edges'),
        ('type6', 'Type 6 - Fluffy pieces with ragged edges'),
        ('type7', 'Type 7 - Entirely liquid'),
    ]
    
    stool_type = models.CharField(max_length=10, choices=STOOL_TYPES)
    pain = models.BooleanField(default=False, help_text="Check if experiencing pain")
    blood_in_stool = models.BooleanField(default=False, help_text="Check if blood is visible in the stool")
    blood_on_paper = models.BooleanField(default=False, help_text="Check if blood is visible on toilet paper")
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        username = self.user.username if self.user.username else f"User {self.user.id}"
        return f"{username}: {self.get_stool_type_display()} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
