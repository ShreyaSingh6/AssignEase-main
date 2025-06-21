from django.shortcuts import render

# Create your views here.

def notes_home(request):
    return render(request, 'notes_home.html')
