import mimetypes
import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from Home.models import Teacher, Student
from Admin.models import Assignment, Subject
from Student.models import Student_Assignment
from django.core.mail import EmailMessage
from django.conf import settings
from Home.models import CourseSectionInfo 


# Create your views here.

def Teacher_Home(request):
    if request.session.has_key('Teacher_email'):
        ems = request.session['Teacher_email']
        T_obj = Teacher.objects.filter(Email=ems)
        return render(request, 'Teacher_Dashboard.html', {'msgT': T_obj, 'temail': ems})
    else:
        return render(request, 'Home.html')


# -------Teacher UPDATE PASSWORD------------

def TeacherUpdate_Password(request):
    if request.session.has_key('Teacher_email'):
        ems = request.session['Teacher_email']
        return render(request, 'TeacherUpdatePassword.html', {'msg1': ems})
    else:
        return render(request, 'Home.html')


def change_pass_Teacher(request):
    if request.session.has_key('Teacher_email'):
        Current_user = request.session['Teacher_email']
        Old_Password = request.POST['Old_p']
        New_Password = request.POST['New_p']
        Confirm_Password = request.POST['Confirm_p']
        signup_objt = Teacher.objects.filter(Email=Current_user, Password=Old_Password)
        data_len = len(signup_objt)
        if data_len == 1:
            if New_Password == Confirm_Password:
                for my in signup_objt:
                    Login_id = my.id
                    signup_obj1 = Teacher.objects.get(id=Login_id)
                    signup_obj1.Password = New_Password
                    signup_obj1.save()
                    return render(request, 'Home.html', {'set_msg1': 'Password Changed Successfully'})
            else:
                return render(request, 'TeacherUpdatePassword.html',
                              {'msg11': 'New and Confirm Password does not match !'})
        else:
            return render(request, 'TeacherUpdatePassword.html', {'msg22': 'Old Password Incorrect'})
    else:
        return render(request, 'Home.html')


# Student Report ------code--------------------------

def StudentReport(request):
    if request.session.has_key('Teacher_email'):
        a = request.session['Teacher_email']
        data_obj = Student.objects.all()
        return render(request, 'Student_report.html', {'data': data_obj})
    else:
        return render(request, 'Home.html')


# ----------------------------------------------------------------------
# Teacher Image

def Teacher_image(request):
    if request.session.has_key('Teacher_email'):
        ems = request.session['Teacher_email']
        Teacher_data = Teacher.objects.filter(Email=ems)
        return render(request, 'Teacherpicture.html', {'Teacher_data': Teacher_data})
    else:
        return render(request, 'Home.html')


#  Teacher Image Upload
def Teacher_Upload_img(request):
    if request.session.has_key('Teacher_email'):
        ems = request.session['Teacher_email']
        if request.method == 'POST' and request.FILES['img_stu']:
            Name = request.POST['nm']
            filedata = request.FILES['img_stu']
            st = FileSystemStorage()
            filename = st.save(filedata.name, filedata)
            my_file_uploaded_url = st.url(filename)
            data_obj = Teacher.objects.get(Name=Name)
            data_obj.Image = my_file_uploaded_url
            data_obj.save()

            return render(request, 'Teacherpicture.html', {'pic': data_obj})
    else:
        return render(request, 'Home.html')


# Assignment Add-----------------------------------------

def Assignment_Add_p(request):
    if request.session.has_key('Teacher_email'):
        subject = request.session['Teacher_email']
        return render(request, 'Assignment_Add.html', {'data': subject})
    else:
        return render(request, 'Home.html')


def Assignment_Add(request):
    
    if request.session.has_key('Teacher_email'):
        ems = request.session['Teacher_email']
        if request.method == 'POST' and request.FILES['ass_stu']:
            Subject_Name = request.POST['SN']
            Assignment_Title = request.POST['AT']
            Assignment_Description = request.POST['AD']
            Due_Date = request.POST['DD']

            filedata = request.FILES['ass_stu']
            st = FileSystemStorage()
            filename = st.save(filedata.name, filedata)
            my_file_uploaded_url = st.url(filename)

            data_obj = Assignment(Subject_Name=Subject_Name, Assignment_Title=Assignment_Title,
                                  Assignment_Description=Assignment_Description, Due_Date=Due_Date,
                                  Assignment_File=my_file_uploaded_url, File_Name=filename)
            data_obj.save()

            # Get all student emails
            student_emails = list(Student.objects.values_list('Email', flat=True))

            # Prepare the email
            subject = f'New Assignment Uploaded: {Assignment_Title}'
            message = f'''
Dear Student,

A new assignment has been uploaded by your teacher.

Subject: {Subject_Name}
Title: {Assignment_Title}
Description: {Assignment_Description}
Due Date: {Due_Date}

Please check your portal for more details.

Regards,
{ems}
            '''

            try:
                email = EmailMessage(
                    subject,
                    message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[],
                    bcc=student_emails,
                )
                email.send(fail_silently=False)
            except Exception as e:
                print("Mail sending error:", e)




            return render(request, 'Assignment_Add.html', {'ass': data_obj})

    return render(request, 'Home.html')


# Subject Add--------------------
def Subject_Add_P(request):
    if request.session.has_key('Teacher_email'):
        subject = request.session['Teacher_email']
        return render(request, 'Subject_Add.html', {'data': subject})
    else:
        return render(request, 'Home.html')


def Subject_Add(request):
    Subject_Name = request.POST['sn']
    Subject_Description = request.POST['sd']
    signup_obj = Subject(Subject_Name=Subject_Name, Subject_Description=Subject_Description)
    signup_obj.save()
    return render(request, 'Subject_Add.html', {"msgs": "Subject Added Successfully"})


# Subject Report ------code--------------------------

def Subject_Report(request):
    if request.session.has_key('Teacher_email'):
        a = request.session['Teacher_email']
        data_obj = Subject.objects.all()
        return render(request, 'Subject_report.html', {'data': data_obj})
    else:
        return render(request, 'Home.html')


# Assignment Report ------code--------------------------

def Assignment_Report(request):
    if request.session.has_key('Teacher_email'):
        a = request.session['Teacher_email']
        data_obj = Assignment.objects.all()
        return render(request, 'Assignment_Report.html', {'data': data_obj})
    else:
        return render(request, 'Home.html')


# --------------------Submitted Assignment Download---------------------

def View_Stu_Ass(request):
    if request.session.has_key('Teacher_email'):
        a = request.session['Teacher_email']
        data_obj = Student_Assignment.objects.all()
        return render(request, 'Submitted_Assignment.html', {'data': data_obj})
    else:
        return render(request, 'Home.html')


def download_Assignment_S(request):
    user_id = request.GET.get('ids')
    obj = Student_Assignment.objects.get(id=user_id)
    file_name = obj.File_Name  # Use directly unless you know it has slashes
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(file_path):
        return HttpResponse("File not found.", status=404)

    wrapper = FileWrapper(open(file_path, 'rb'))
    content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    response['Content-Length'] = os.path.getsize(file_path)
    return response


def my_acc(request):
    if request.session.has_key('Teacher_email'):
        ems = request.session['Teacher_email']
        Teacher_data = Teacher.objects.filter(Email=ems)
        return render(request, 'My_acc.html', {'Teacher_data': Teacher_data})
    else:
        return render(request, 'Home.html')


def Grade_Assignment(request, id):
    if request.method == 'POST':
        marks = int(request.POST.get('marks'))
        
        # Assign grade based on marks
        if marks >= 90:
            grade = 'A+'
        elif marks >= 80:
            grade = 'A'
        elif marks >= 70:
            grade = 'B'
        elif marks >= 60:
            grade = 'C'
        elif marks >= 50:
            grade = 'D'
        elif marks >= 40:
            grade = 'E'
        else:
            grade = 'F'

        assignment = Student_Assignment.objects.get(id=id)
        assignment.Marks = marks
        assignment.Grade = grade
        assignment.save()

    return redirect('View_Stu_Ass')  # change as per your actual view name
