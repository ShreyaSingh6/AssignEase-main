from django import forms
from .models import Student_Assignment

class StudentAssignmentForm(forms.ModelForm):
    class Meta:
        model = Student_Assignment
        fields = ['Subject_Name', 'Assignment_Title', 'Assignment_Description', 'Submission_Date']

