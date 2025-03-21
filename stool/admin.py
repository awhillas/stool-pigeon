from django.contrib import admin
from .models import StoolRecord

@admin.register(StoolRecord)
class StoolRecordAdmin(admin.ModelAdmin):
    list_display = ('stool_type', 'timestamp')
    list_filter = ('stool_type', 'timestamp')
    search_fields = ('stool_type',)
