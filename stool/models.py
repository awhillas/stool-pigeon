from django.db import models
from django.utils import timezone

class StoolRecord(models.Model):
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
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.get_stool_type_display()} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
