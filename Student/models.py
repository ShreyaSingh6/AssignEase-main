from django.db import models

# Create your models here.

class Student_Assignment(models.Model):
    Roll = models.CharField(max_length=50, default='unknown')
    Subject_Name = models.CharField(max_length=200)
    Assignment_Title = models.CharField(max_length=200)
    Assignment_Description = models.CharField(max_length=200)
    File_Name = models.CharField(max_length=200)
    Submission_Date = models.CharField(max_length=200)
    Marks = models.IntegerField(null=True, blank=True)
    Grade = models.CharField(max_length=2, null=True, blank=True)


