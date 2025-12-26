# courses/forms.py

from django import forms
from .models import Course, Lesson, Category

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'slug', 'description', 'short_description',
            'category', 'level', 'price', 'discount_price',
            'thumbnail', 'duration_hours', 'is_free', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'short_description': forms.Textarea(attrs={'rows': 3}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'slug', 'content', 'video_url', 
                 'duration_minutes', 'order', 'is_free_preview']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }