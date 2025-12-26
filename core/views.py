# core/views.py

from django.shortcuts import render
from courses.models import Course

def home(request):
    featured_courses = Course.objects.filter(
        status='published', 
        is_featured=True
    )[:6]
    
    latest_courses = Course.objects.filter(
        status='published'
    ).order_by('-created_at')[:6]
    
    context = {
        'featured_courses': featured_courses,
        'latest_courses': latest_courses,
    }
    
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')