from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Student, Attendance, Branch, Year, Section
from django.utils import timezone
from datetime import datetime
import qrcode
import socket
from StudentView.views import present


def qrgenerator():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]

    link = f"http://{ip}:8000/add_manually"

    # Function to generate and display a QR code
    def generate_qr_code(link):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("FacultyView/static/FacultyView/qrcode.png")

    generate_qr_code(link)


def get_class_wise_distribution():
    """Get class-wise student distribution"""
    distribution = []
    branches = Branch.objects.all()
    years = Year.objects.all().order_by('year')
    sections = Section.objects.all().order_by('section')
    
    for branch in branches:
        for year in years:
            for section in sections:
                students = Student.objects.filter(
                    s_branch=branch,
                    s_year=year,
                    s_section=section
                ).count()
                if students > 0:
                    distribution.append({
                        'class_name': f"{branch.branch} {year.year} {section.section}",
                        'branch': branch.branch,
                        'year': year.year,
                        'section': section.section,
                        'student_count': students,
                        'branch_id': branch.id,
                        'year_id': year.id,
                        'section_id': section.id,
                    })
    return distribution


def faculty_view(request):
    if request.method == "POST":
        if "student_id" in request.POST:
            # Remove student from present list
            student_roll = request.POST["student_id"]
            student = Student.objects.get(s_roll=student_roll)
            if student in present:
                present.remove(student)
            return HttpResponseRedirect("/")
        
        elif "submit_attendance" in request.POST:
            # Save all present students to database with today's date
            today = timezone.now().date()
            for student in present:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'is_present': True}
                )
            present.clear()
            return HttpResponseRedirect("/attendance_submitted")

    else:
        qrgenerator()
        
        # Get unique dates for filtering
        dates = Attendance.objects.dates('date', 'day', order='DESC')
        selected_date = request.GET.get('date')
        
        if selected_date:
            try:
                filter_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
                attendance_records = Attendance.objects.filter(date=filter_date, is_present=True).select_related('student')
                students_with_attendance = [record.student for record in attendance_records]
            except ValueError:
                students_with_attendance = []
        else:
            students_with_attendance = []
        
        return render(
            request,
            "FacultyView/FacultyViewIndex.html",
            {
                "students": present,
                "attendance_dates": dates,
                "selected_date": selected_date,
                "students_with_attendance": students_with_attendance,
            },
        )


def add_manually(request):
    students = Student.objects.all().order_by("s_roll")
    return render(
        request,
        "StudentView/StudentViewIndex.html",
        {
            "students": students,
        },
    )


def attendance_submitted(request):
    return render(request, "FacultyView/AttendanceSubmitted.html")


def class_distribution(request):
    """View for class-wise student distribution"""
    distribution = get_class_wise_distribution()
    branches = Branch.objects.all().values_list('branch', flat=True).distinct()
    total_students = Student.objects.count()
    total_classes = len(distribution)
    
    # Calculate average per class
    average_per_class = total_students // total_classes if total_classes > 0 else 0
    
    return render(
        request,
        "FacultyView/ClassDistribution.html",
        {
            "distribution": distribution,
            "branches": list(branches),
            "total_students": total_students,
            "total_classes": total_classes,
            "average_per_class": average_per_class,
        },
    )


def class_students(request, branch_id, year_id, section_id):
    """View for students in a specific class"""
    try:
        branch = Branch.objects.get(id=branch_id)
        year = Year.objects.get(id=year_id)
        section = Section.objects.get(id=section_id)
        
        students = Student.objects.filter(
            s_branch=branch,
            s_year=year,
            s_section=section
        ).order_by('s_roll')
        
        # Get attendance stats for these students
        attendance_stats = {}
        for student in students:
            count = Attendance.objects.filter(
                student=student,
                is_present=True
            ).count()
            attendance_stats[student.s_roll] = count
        
        return render(
            request,
            "FacultyView/ClassStudents.html",
            {
                "class_name": f"{branch.branch} Year {year.year} Section {section.section}",
                "students": students,
                "attendance_stats": attendance_stats,
                "branch": branch.branch,
                "year": year.year,
                "section": section.section,
            },
        )
    except (Branch.DoesNotExist, Year.DoesNotExist, Section.DoesNotExist):
        return HttpResponseRedirect("/class_distribution")
