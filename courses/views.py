# courses/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Course, Lesson, Category, Enrollment
from .forms import CourseForm, LessonForm

def course_list(request):
    courses = Course.objects.filter(status='published')
    categories = Category.objects.all()
    
    context = {
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, status='published')
    lessons = course.lessons.all()
    
    # Проверяем, зачислен ли пользователь на курс
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user, 
            course=course
        ).exists()
    
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def create_course(request):
    if not request.user.is_teacher():
        return HttpResponseForbidden("Только преподаватели могут создавать курсы")
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Курс создан успешно!')
            return redirect('course_detail', slug=course.slug)
    else:
        form = CourseForm()
    
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def add_lesson(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    
    # Проверяем, является ли пользователь инструктором курса
    if course.instructor != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Вы не можете добавлять уроки к этому курсу")
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, 'Урок добавлен успешно!')
            return redirect('course_detail', slug=course.slug)
    else:
        form = LessonForm()
    
    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'courses/add_lesson.html', context)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, status='published')
    
    # Создаем запись о зачислении
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    
    if created:
        course.students.add(request.user)
        messages.success(request, f'Вы успешно записались на курс "{course.title}"')
    else:
        messages.info(request, f'Вы уже записаны на курс "{course.title}"')
    
    return redirect('course_detail', slug=course.slug)