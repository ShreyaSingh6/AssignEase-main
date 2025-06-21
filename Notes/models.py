from django.db import models

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    CATEGORY_CHOICES = [
        ('notes', 'Notes'),
        ('pyq', 'Previous Year Question'),
        ('syllabus', 'Syllabus')
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    uploaded_by = models.CharField(max_length=100)  # email or username
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    file = models.FileField(upload_to='notes/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.category} - {self.uploaded_by}"
