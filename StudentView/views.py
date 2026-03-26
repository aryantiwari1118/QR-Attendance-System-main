from django.shortcuts import render
from FacultyView.models import Student, Attendance
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

# Create your views here.

present = set()


def add_manually_post(request):
    student_roll = request.POST["student-name"]
    student = Student.objects.get(s_roll=student_roll)
    present.add(student)
    
    # Save to database with today's date
    today = timezone.now().date()
    Attendance.objects.update_or_create(
        student=student,
        date=today,
        defaults={'is_present': True}
    )
    
    return HttpResponseRedirect("/submitted")


def submitted(request):
    return render(request, "StudentView/Submitted.html")
