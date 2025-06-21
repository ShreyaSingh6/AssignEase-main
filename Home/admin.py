from django.contrib import admin

# Register your models here.
from .models import Admin, Student, Teacher
from .models import CourseSectionInfo

admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(CourseSectionInfo)

