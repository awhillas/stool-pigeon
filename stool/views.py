from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import StoolRecord
from .forms import StoolRecordForm
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import timedelta
from collections import defaultdict


def get_stool_stats_context(user):
    """Helper function to generate statistics context for a user"""
    try:
        import numpy as np
    except ImportError:
        return {'stats_available': False}
    
    # Get the current date and time
    now = timezone.now()
    
    # Calculate dates for week and month ranges
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # Get all records from the last month for current user
    month_records = StoolRecord.objects.filter(timestamp__gte=month_ago, user=user)
    week_records = month_records.filter(timestamp__gte=week_ago)
    
    # Calculate records per day for last week
    week_data = defaultdict(int)
    for i in range(7):
        day = now - timedelta(days=i)
        date_str = day.strftime('%Y-%m-%d')
        week_data[date_str] = 0  # Initialize all days with zero
    
    # Count records by day for the week
    for record in week_records:
        date_str = record.timestamp.strftime('%Y-%m-%d')
        week_data[date_str] += 1
    
    # Calculate records per day for last month
    month_data = defaultdict(int)
    for i in range(30):
        day = now - timedelta(days=i)
        date_str = day.strftime('%Y-%m-%d')
        month_data[date_str] = 0  # Initialize all days with zero
    
    # Count records by day for the month
    for record in month_records:
        date_str = record.timestamp.strftime('%Y-%m-%d')
        month_data[date_str] += 1
    
    # Calculate statistics
    week_values = list(week_data.values())
    month_values = list(month_data.values())
    
    try:
        # Calculate mean and standard deviation
        week_mean = np.mean(week_values) if week_values else 0
        week_std = np.std(week_values) if week_values else 0
        month_mean = np.mean(month_values) if month_values else 0
        month_std = np.std(month_values) if month_values else 0
    except Exception:
        # Fallback to basic statistics if numpy fails
        week_mean = sum(week_values) / len(week_values) if week_values else 0
        week_std = 0  # Simplified fallback
        month_mean = sum(month_values) / len(month_values) if month_values else 0
        month_std = 0  # Simplified fallback
    
    return {
        'week_mean': round(week_mean, 2),
        'week_std': round(week_std, 2),
        'month_mean': round(month_mean, 2),
        'month_std': round(month_std, 2),
        'week_total': sum(week_values),
        'month_total': sum(month_values),
        'stats_available': True,
    }


@login_required
def home(request):
    # Get records for the current logged-in user only
    records = StoolRecord.objects.filter(user=request.user).order_by('-timestamp')[:10]
    
    # Get the last record to use as default values for the form
    last_record = None
    if records.exists():
        last_record = records.first()
    
    # Handle form submission
    if request.method == 'POST':
        form = StoolRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('stool:home')
    else:
        # Initialize form with last record values if available
        initial_data = {}
        if last_record:
            initial_data = {
                'stool_type': last_record.stool_type,
                'pain': last_record.pain,
                'blood_in_stool': last_record.blood_in_stool,
                'blood_on_paper': last_record.blood_on_paper,
            }
        form = StoolRecordForm(initial=initial_data)
    
    # Get statistics for display
    stats_context = get_stool_stats_context(request.user)
    
    # Get total records count
    total_records = StoolRecord.objects.filter(user=request.user).count()
    
    context = {
        'records': records,
        'form': form,
        'last_record': last_record,
        'stats': stats_context,
        'total_records': total_records,
    }
    return render(request, 'stool/home.html', context)


@login_required 
def stool_stats(request):
    """Returns statistics about stool frequency for the dashboard"""
    context = get_stool_stats_context(request.user)
    return render(request, 'stool/partials/stool_stats.html', context)
