from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import StoolRecord
from django.utils import timezone
from django.template.loader import render_to_string

@login_required
def home(request):
    # Get records for the current logged-in user only
    records = StoolRecord.objects.filter(user=request.user).order_by('-timestamp')[:10]
    
    # Get the last record to use as default values for the form
    last_record = None
    if records.exists():
        last_record = records.first()
    
    context = {
        'records': records,
        'stool_types': StoolRecord.STOOL_TYPES,
        'last_record': last_record,
    }
    return render(request, 'stool/home.html', context)

@login_required
def add_record(request):
    """View to handle adding a new stool record"""
    if request.method == 'POST':
        # Debug - log the request
        print(f"Received POST request. Is HTMX: {getattr(request, 'htmx', False)}")
        print(f"POST data: {dict(request.POST)}")
            
        # Get the form data
        stool_type = request.POST.get('stool_type')
        pain = request.POST.get('pain') == 'on'
        blood_in_stool = request.POST.get('blood_in_stool') == 'on'
        blood_on_paper = request.POST.get('blood_on_paper') == 'on'
        
        if stool_type:
            # Create a new stool record in the database
            try:
                record = StoolRecord.objects.create(
                    user=request.user,
                    stool_type=stool_type, 
                    pain=pain,
                    blood_in_stool=blood_in_stool,
                    blood_on_paper=blood_on_paper
                )
                print(f"Created new record with ID: {record.id}, type: {record.stool_type}")
                
                # Get latest records for the current user
                records = StoolRecord.objects.filter(user=request.user).order_by('-timestamp')[:10]
                
                # Handle HTMX request
                if getattr(request, 'htmx', False):
                    context = {
                        'records': records,
                        'new_record_id': record.id
                    }
                    html = render_to_string('stool/partials/records_list.html', context, request=request)
                    # Create response with the updated records list
                    response = HttpResponse(html)
                    
                    # Trigger multiple event types to ensure stats update
                    # Include a human-readable timestamp 
                    formatted_time = record.timestamp.strftime('%b %d, %Y %I:%M %p')
                    response['HX-Trigger'] = '{"recordAdded": {"id": ' + str(record.id) + ', "refresh": true}, "refreshStats": true, "stoolRecordAdded": {"id": ' + str(record.id) + ', "type": "' + stool_type + '", "pain": ' + str(pain).lower() + ', "blood_in_stool": ' + str(blood_in_stool).lower() + ', "blood_on_paper": ' + str(blood_on_paper).lower() + ', "timestamp": "' + formatted_time + '"}}'
                    
                    # Add debugging headers
                    response['HX-Debug'] = 'true'
                    response['X-Record-Created'] = 'true'
                    
                    return response
                
                # Handle regular form submission (non-HTMX)
                return redirect('stool:home')
            
            except Exception as e:
                print(f"Error creating record: {str(e)}")
                if getattr(request, 'htmx', False):
                    return HttpResponse(f"Error creating record: {str(e)}", status=500)
                return redirect('stool:home')
                
        else:
            print("No stool type provided in request")
            if getattr(request, 'htmx', False):
                return HttpResponse("No stool type selected", status=400)
            return redirect('stool:home')
            
    # Method not allowed
    print(f"Invalid request method: {request.method}")
    return HttpResponse("Method not allowed", status=405)

@login_required
def records_list(request):
    """View to render just the records list for HTMX partial updates"""
    records = StoolRecord.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'stool/partials/records_list.html', {'records': records})

@login_required
def records_count(request):
    """Return the total count of records for the current user"""
    count = StoolRecord.objects.filter(user=request.user).count()
    return HttpResponse(f'<i class="bi bi-database me-1"></i> {count} total')

@login_required
def stool_stats(request):
    """Returns statistics about stool frequency for the dashboard"""
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count
    from collections import defaultdict
    
    # Check for various HTMX request types
    is_htmx = getattr(request, 'htmx', False) or request.headers.get('HX-Request') == 'true'
    htmx_trigger = request.headers.get('HX-Trigger', '')
    is_custom_event = 'stoolRecordAdded' in htmx_trigger
    print(f"HTMX: {is_htmx}, Trigger: {htmx_trigger}, Custom Event: {is_custom_event}")
    
    try:
        import numpy as np
        print("Successfully imported numpy")
    except ImportError as e:
        print(f"Error importing numpy: {e}")
        # Fallback if numpy is not available
        return HttpResponse("<div class='p-4 text-center'>Statistics module not available</div>")
    
    # Get the current date and time
    now = timezone.now()
    
    # Calculate dates for week and month ranges
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # Get all records from the last month for current user
    month_records = StoolRecord.objects.filter(timestamp__gte=month_ago, user=request.user)
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
    
    # Debug output
    print(f"Week data: {week_values}")
    print(f"Month data: {month_values}")
    
    try:
        # Calculate mean and standard deviation
        week_mean = np.mean(week_values) if week_values else 0
        week_std = np.std(week_values) if week_values else 0
        month_mean = np.mean(month_values) if month_values else 0
        month_std = np.std(month_values) if month_values else 0
        print(f"Statistics calculated - Week mean: {week_mean}, std: {week_std}")
        print(f"Statistics calculated - Month mean: {month_mean}, std: {month_std}")
    except Exception as e:
        print(f"Error calculating statistics: {e}")
        # Fallback to basic statistics if numpy fails
        week_mean = sum(week_values) / len(week_values) if week_values else 0
        week_std = 0  # Simplified fallback
        month_mean = sum(month_values) / len(month_values) if month_values else 0
        month_std = 0  # Simplified fallback
    
    # Prepare data for template
    context = {
        'week_mean': round(week_mean, 2),
        'week_std': round(week_std, 2),
        'month_mean': round(month_mean, 2),
        'month_std': round(month_std, 2),
        'week_total': sum(week_values),
        'month_total': sum(month_values),
        'now': now,
        'is_update': is_custom_event,
    }
    
    response = render(request, 'stool/partials/stool_stats.html', context)
    
    # Add debugging headers for HTMX requests
    if is_htmx:
        response['HX-Debug'] = 'true'
        response['X-Stats-Generated'] = 'true'
        
        # Add special header for custom events
        if is_custom_event:
            response['X-Triggered-By'] = 'stoolRecordAdded'
    
    return response
