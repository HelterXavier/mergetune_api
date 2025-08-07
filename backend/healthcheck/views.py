from os import times
from django.shortcuts import render
from django.http import JsonResponse
import pytz
from datetime import datetime

def health_check(request):
    tz = pytz.timezone('UTC')
    date_now = datetime.now(tz)
    
    hour = date_now.hour
    
    if 5 <= hour < 12:
        greeting = "Good morning! The server is running smoothly."
    elif 12 <= hour < 17:
        greeting = "Good afternoon! The server is running smoothly."
    elif 17 <= hour < 22:
        greeting = "Good evening! The server is running smoothly."
    else:
        greeting = "Good night! The server is running smoothly."
        
    message = f"{greeting}"
    timestamp = date_now.strftime('%Y-%m-%d %H:%M:%S %Z')
    
    context = {
        'message': message,
        'last_updated': timestamp,
        'version': '1.0.0',
    }
    
    return render(request, 'healthcheck/health_check.html', context)