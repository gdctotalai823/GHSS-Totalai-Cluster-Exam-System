from django.db import models
from apps.schools.models import School, Class, Section

class ExaminationSession(models.Model):
    title = models.CharField(max_length=100, help_text='e.g., 2024-2025')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Examination Session'
        verbose_name_plural = 'Examination Sessions'

    def __str__(self):
        return self.title


class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('I', 'Semester I'),
        ('II', 'Semester II'),
    ]
    
    exam_session = models.ForeignKey(ExaminationSession, on_delete=models.CASCADE, related_name='semesters')
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    weightage = models.IntegerField(help_text='Weightage percentage')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['exam_session', 'semester']
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'
        unique_together = ['exam_session', 'semester']

    def __str__(self):
        return f"{self.exam_session.title} - Semester {self.semester}"
