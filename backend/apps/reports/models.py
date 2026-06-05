from django.db import models
from apps.students.models import Student
from apps.examinations.models import ExaminationSession

class RollNumberSlip(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='roll_slips')
    exam_session = models.ForeignKey(ExaminationSession, on_delete=models.CASCADE, related_name='roll_slips')
    
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    is_printed = models.BooleanField(default=False)
    printed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-generated_at']
        unique_together = ['student', 'exam_session']

    def __str__(self):
        return f"Roll Slip - {self.student.name}"


class DMC(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='dmcs')
    result = models.OneToOneField('results.Result', on_delete=models.CASCADE, related_name='dmc')
    
    qr_code = models.CharField(max_length=255, unique=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    is_printed = models.BooleanField(default=False)
    printed_at = models.DateTimeField(null=True, blank=True)
    print_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"DMC - {self.student.name}"


class Gazette(models.Model):
    GAZETTE_TYPE_CHOICES = [
        ('school', 'School-Wise Gazette'),
        ('class', 'Class-Wise Gazette'),
        ('cluster', 'Cluster Gazette'),
    ]
    
    exam_session = models.ForeignKey(ExaminationSession, on_delete=models.CASCADE, related_name='gazettes')
    gazette_type = models.CharField(max_length=20, choices=GAZETTE_TYPE_CHOICES)
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, null=True, blank=True)
    class_obj = models.ForeignKey('schools.Class', on_delete=models.CASCADE, null=True, blank=True)
    
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.get_gazette_type_display()} - {self.exam_session.title}"


class MeritList(models.Model):
    MERIT_TYPE_CHOICES = [
        ('school', 'School-Wise Merit'),
        ('class', 'Class-Wise Merit'),
        ('cluster', 'Cluster-Wide Merit'),
    ]
    
    exam_session = models.ForeignKey(ExaminationSession, on_delete=models.CASCADE, related_name='merit_lists')
    merit_type = models.CharField(max_length=20, choices=MERIT_TYPE_CHOICES)
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, null=True, blank=True)
    class_obj = models.ForeignKey('schools.Class', on_delete=models.CASCADE, null=True, blank=True)
    
    top_count = models.IntegerField(default=20)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.get_merit_type_display()} - {self.exam_session.title}"


class StatisticalReport(models.Model):
    exam_session = models.ForeignKey(ExaminationSession, on_delete=models.CASCADE, related_name='statistics')
    
    total_schools = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    total_passed = models.IntegerField(default=0)
    total_failed = models.IntegerField(default=0)
    pass_percentage = models.FloatField(default=0)
    
    data = models.JSONField(default=dict)
    
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-generated_at']
        unique_together = ['exam_session']

    def __str__(self):
        return f"Statistics - {self.exam_session.title}"
