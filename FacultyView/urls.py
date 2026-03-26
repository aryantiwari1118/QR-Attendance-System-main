from . import views
from django.urls import path

urlpatterns = [
    path("", views.faculty_view, name="faculty_view"),
    path("add_manually", views.add_manually, name="add_manually"),
    path("attendance_submitted", views.attendance_submitted, name="attendance_submitted"),
    path("class_distribution", views.class_distribution, name="class_distribution"),
    path("class_students/<int:branch_id>/<int:year_id>/<int:section_id>", views.class_students, name="class_students"),
]
