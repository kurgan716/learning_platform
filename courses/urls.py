# courses/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.create_course, name='create_course'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/add-lesson/', views.add_lesson, name='add_lesson'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
]