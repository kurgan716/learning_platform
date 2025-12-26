# courses/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(unique=True, verbose_name='URL')
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    )
    
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    short_description = models.CharField(max_length=300, verbose_name='Краткое описание')
    
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_created',
        limit_choices_to={'role': 'teacher'},
        verbose_name='Преподаватель'
    )
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Категория'
    )
    
    level = models.CharField(
        max_length=20, 
        choices=LEVEL_CHOICES, 
        default='beginner',
        verbose_name='Уровень сложности'
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name='Статус'
    )
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name='Цена'
    )
    
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name='Цена со скидкой'
    )
    
    thumbnail = models.ImageField(
        upload_to='course_thumbnails/', 
        blank=True, 
        null=True,
        verbose_name='Изображение'
    )
    
    duration_hours = models.PositiveIntegerField(
        default=0,
        verbose_name='Продолжительность (часов)'
    )
    
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='courses_enrolled',
        blank=True,
        verbose_name='Студенты'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    published_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата публикации')
    
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемый')
    is_free = models.BooleanField(default=False, verbose_name='Бесплатный')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def current_price(self):
        return self.discount_price if self.discount_price else self.price

class Lesson(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='lessons',
        verbose_name='Курс'
    )
    
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    video_url = models.URLField(blank=True, verbose_name='Видео URL')
    duration_minutes = models.PositiveIntegerField(
        default=0,
        verbose_name='Продолжительность (минут)'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_free_preview = models.BooleanField(
        default=False,
        verbose_name='Бесплатный предварительный просмотр'
    )
    
    class Meta:
        ordering = ['order']
        unique_together = ['course', 'slug']
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name='Студент'
    )
    
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    
    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата записи'
    )
    
    completed = models.BooleanField(
        default=False,
        verbose_name='Завершено'
    )
    
    completed_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Дата завершения'
    )
    
    class Meta:
        unique_together = ['student', 'course']
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"