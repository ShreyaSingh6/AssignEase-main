from django.shortcuts import render, redirect
from Home.models import Student
from .models import Student_Assignment
from Admin.models import Subject, Assignment
import mimetypes
import os
from wsgiref.util import FileWrapper
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from django.core.files.storage import FileSystemStorage
from .forms import StudentAssignmentForm


# Create your views here.

# def home(request):
#     return render(request, 'Home.html')
# student/views.py


def download_Assignment_T(request):
    try:
        assignment_id = request.GET['ids']
        obj = Assignment.objects.get(id=assignment_id)

        # Fix: Strip any leading '/media/' or slashes
        cleaned_filename = obj.File_Name.replace('/media/', '').lstrip('/\\')

        file_path = os.path.join(settings.MEDIA_ROOT, cleaned_filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError

        mime_type, _ = mimetypes.guess_type(file_path)
        response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response

    except (Assignment.DoesNotExist, KeyError, FileNotFoundError):
        raise Http404("File not found.")


def Student_dashboard(request):
    if request.session.has_key('Student_email'):
        ems = request.session['Student_email']
        return render(request, 'Student_Dashboard.html')
    else:
        return render(request, 'Home.html')


# -------Student UPDATE PASSWORD------------

def StudentUpdate_Password(request):
    if request.session.has_key('Student_email'):
        ems = request.session['Student_email']
        return render(request, 'StudentUpdatePassword.html', {'msg1': ems})
    else:
        return render(request, 'Home.html')


def change_pass_student(request):
    if request.session.has_key('Student_email'):
        Current_user = request.session['Student_email']
        Old_Password = request.POST['Old_p']
        New_Password = request.POST['New_p']
        Confirm_Password = request.POST['Confirm_p']
        signup_objk = Student.objects.filter(Email=Current_user, Password=Old_Password)
        data_len = len(signup_objk)
        if data_len == 1:
            if New_Password == Confirm_Password:
                for my in signup_objk:
                    Login_id = my.id
                    signup_obj1 = Student.objects.get(id=Login_id)
                    signup_obj1.Password = New_Password
                    signup_obj1.save()
                    return render(request, 'Home.html', {'set_msg1': 'Password Changed Successfully'})
            else:
                return render(request, 'StudentUpdatePassword.html',
                              {'msg11': 'New and Confirm Password does not match !'})
        else:
            return render(request, 'StudentUpdatePassword.html', {'msg22': 'Old Password Incorrect'})
    else:
        return render(request, 'Home.html')


# User Profile picture Data

def data_save(request):
    if request.session.has_key('Student_email'):
        ems = request.session['Student_email']
        Student_data = Student.objects.filter(Email=ems)
        return render(request, 'Studentpicture.html', {'Student_data': Student_data})
    else:
        return render(request, 'Home.html')


def Upload_image(request):
    if request.session.has_key('Student_email'):
        ems = request.session['Student_email']
        if request.method == 'POST' and request.FILES['img_stu']:
            Name = request.POST['nm']
            filedata = request.FILES['img_stu']
            st = FileSystemStorage()
            filename = st.save(filedata.name, filedata)
            my_file_uploaded_url = st.url(filename)

            data_obj = Student.objects.get(Name=Name)
            data_obj.Image = my_file_uploaded_url
            data_obj.save()
            return render(request, 'Studentpicture.html', {'pic': data_obj})
    else:
        return render(request, 'Home.html')


# ---------------------------------------------------------------------------

def Subject_List(request):
    if request.session.has_key('Student_email'):
        data_obj = request.session['Student_email']
        data_obj = Subject.objects.all()
        return render(request, 'Subject_List.html', {'data': data_obj})
    else:
        return render(request, 'Home.html')


# Assignment list---------------------

def Assignment_List(request):
    if request.session.has_key('Student_email'):
        a = request.session['Student_email']
        data_obj = Assignment.objects.all()
        return render(request, 'Assignment_list.html', {'data': data_obj})
    else:
        return render(request, 'Home.html')


# --------------------Assignment Download---------------------

def download_myfile(request):
    user_id = request.GET['ids']
    obj = Assignment.objects.get(id=user_id)
    file_name = obj.File_Name
    file_path = settings.MEDIA_ROOT + '/' + file_name
    file_wrapper = FileWrapper(open(file_path, 'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % str(file_name)
    return response


def Submit_Assignment_P(request):
    if request.session.has_key('Student_email'):
        assignments = Assignment.objects.all()  # Filter by subject/student if needed
        if request.method == 'POST':
            form = StudentAssignmentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('Submit_Assignment_P')
        else:
            form = StudentAssignmentForm()
        return render(request, 'Submit_Assignment.html', {
            'form': form,
            'data': assignments
        })
    else:
        return render(request, 'Home.html')


from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Student_Assignment
from Teacher.models import Teacher_Assignment
from Home.models import Student

def Submit_Assignment(request):
    if request.session.has_key('Student_email'):
        email = request.session['Student_email']

        try:
            student = Student.objects.get(Email=email)
        except Student.DoesNotExist:
            return render(request, 'Home.html', {'msgg': 'Student not found'})

        roll = student.Roll

        if request.method == 'POST' and request.FILES.get('ass_stu'):
            Subject_Name = request.POST['SN']
            Assignment_Title = request.POST['AT']
            Assignment_Description = request.POST['AD']
            Submission_Date = request.POST['SD']

            filedata = request.FILES['ass_stu']
            st = FileSystemStorage()
            filename = st.save(filedata.name, filedata)

            Student_Assignment.objects.create(
                Subject_Name=Subject_Name,
                Assignment_Title=Assignment_Title,
                Assignment_Description=Assignment_Description,
                Submission_Date=Submission_Date,
                File_Name=filename,
                Roll=roll
            )

            # After successful submission, redirect to the same page with a flag
            return redirect('/Student/Submit_Assignment?submitted=1')

        # GET Request (or after redirect)
        all_assignments = Teacher_Assignment.objects.all()
        submitted_titles = Student_Assignment.objects.filter(Roll =roll).values_list('Assignment_Title', flat=True)
        pending = all_assignments.exclude(Assignment_Title__in=submitted_titles)

        submitted_flag = request.GET.get('submitted') == '1'

        return render(request, 'Submit_Assignment.html', {
            'data': pending,
            'submitted': submitted_flag
        })

    return render(request, 'Home.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from Home.models import Student, CourseSectionInfo

def My_account(request):
    if request.session.has_key('Student_email'):
        ems = request.session['Student_email']
        try:
            student = Student.objects.get(Email=ems)
        except Student.DoesNotExist:
            messages.error(request, "Student not found.")
            return redirect('Student_')

        # POST request: save section
        if request.method == 'POST':
            section = request.POST.get('section')
            if not section:
                messages.error(request, "Please select a valid section.")
                return redirect('My_account')

            student.Section = section
            student.save()
            messages.success(request, "Section updated successfully.")
            return redirect('My_account')

        # Get section range based on Course
        try:
            section_info = CourseSectionInfo.objects.get(Course=student.Course)
            section_range = range(1, section_info.No_of_Sections + 1)
        except CourseSectionInfo.DoesNotExist:
            section_range = []

        return render(request, 'My_account.html', {
            'Student_data': [student],
            'student': student,
            'section_range': section_range
        })

    return redirect('Student_')



def My_Marks(request):
    if request.session.has_key('Student_email'):
        student_email = request.session['Student_email']
        
        try:
            student_obj = Student.objects.get(Email=student_email)
        except Student.DoesNotExist:
            return render(request, 'Home.html', {'error': 'Student not found'})
        
        roll_no = student_obj.Roll

        # Only show assignments submitted by this student that have been graded
        assignments = Student_Assignment.objects.filter(Roll=roll_no, Marks__isnull=False)

        return render(request, 'My_Marks.html', {'assignments': assignments})
    else:
        return render(request, 'Home.html')


