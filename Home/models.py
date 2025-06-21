from django.db import models


# Create your models here.

# Admin Login
class Admin(models.Model):
    Emailid = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)


class Student(models.Model):
    Roll = models.CharField(max_length=50,default='unknown')
    Name = models.CharField(max_length=200)
    Email = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)
    Gender = models.CharField(max_length=200)
    Mobile = models.CharField(max_length=200)
    DOB = models.CharField(max_length=200)
    Course = models.CharField(max_length=200)
    Image = models.CharField(max_length=200)
    Section = models.CharField(max_length=10, null=True, blank=True)


class Teacher(models.Model):
    Roll = models.CharField(max_length=50, default='unknown')
    Name = models.CharField(max_length=200)
    Email = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)
    Gender = models.CharField(max_length=200)
    Mobile = models.CharField(max_length=200)
    DOB = models.CharField(max_length=200)
    Subject = models.CharField(max_length=200)
    Image = models.CharField(max_length=200)

class CourseSectionInfo(models.Model):
    Course = models.CharField(max_length=200, unique=True)
    No_of_Sections = models.IntegerField()

    def __str__(self):
        return f"{self.Course} - {self.No_of_Sections} sections"

