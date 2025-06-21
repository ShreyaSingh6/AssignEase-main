from django.db import models

# Create your models here.
class Teacher_Assignment(models.Model):
    Roll = models.CharField(max_length=50, default='unknown')
    Subject_Name = models.CharField(max_length=200)
    Assignment_Title = models.CharField(max_length=200)
    Assignment_Description = models.CharField(max_length=200)
    File_Name = models.CharField(max_length=200)
    # Assignment_File = models.FileField(upload_to='assignments/')
    Submission_Date = models.CharField(max_length=200)