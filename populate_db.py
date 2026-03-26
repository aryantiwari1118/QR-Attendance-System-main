#!/usr/bin/env python
"""
Script to populate database with sample student data.
Clears existing students and creates 5 students per class.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QR_Attendance_System.settings')
django.setup()

from FacultyView.models import Student, Branch, Year, Section

# First display current data
print("=== Current Database State ===")
print(f"Total Students: {Student.objects.count()}")
print(f"Branches: {list(Branch.objects.values_list('branch', flat=True))}")
print(f"Years: {list(Year.objects.values_list('year', flat=True))}")
print(f"Sections: {list(Section.objects.values_list('section', flat=True))}")

# Clear existing students
print("\n=== Clearing Existing Students ===")
deleted_count, _ = Student.objects.all().delete()
print(f"Deleted {deleted_count} student records")

# Create base data if not exists
branches_data = ['CSE', 'ECE', 'ME']
years_data = [1, 2, 3, 4]
sections_data = ['A', 'B']

print("\n=== Creating Base Data ===")
branches = {}
for branch_name in branches_data:
    b, created = Branch.objects.get_or_create(branch=branch_name)
    branches[branch_name] = b
    print(f"Branch: {branch_name} - {'Created' if created else 'Exists'}")

years = {}
for year_num in years_data:
    y, created = Year.objects.get_or_create(year=year_num)
    years[year_num] = y
    print(f"Year: {year_num} - {'Created' if created else 'Exists'}")

sections = {}
for section_name in sections_data:
    s, created = Section.objects.get_or_create(section=section_name)
    sections[section_name] = s
    print(f"Section: {section_name} - {'Created' if created else 'Exists'}")

# Add sample students
print("\n=== Adding Sample Students ===")
first_names = ['Aarav', 'Bhavika', 'Chirag', 'Deepa', 'Eshan']
last_names = ['Kumar', 'Singh', 'Patel', 'Verma', 'Gupta']

student_count = 0
for branch_name in branches_data:
    for year_num in years_data:
        for section_name in sections_data:
            for i in range(5):
                roll_num = f"{branch_name[0]}{year_num}{section_name}{i+1:02d}"
                first_name = first_names[i]
                last_name = last_names[i]
                
                student = Student.objects.create(
                    s_roll=roll_num,
                    s_fname=first_name,
                    s_lname=last_name,
                    s_branch=branches[branch_name],
                    s_year=years[year_num],
                    s_section=sections[section_name]
                )
                student_count += 1
                print(f"Created: {student}")

print(f"\n=== Summary ===")
print(f"Total new students created: {student_count}")
print(f"Total students in database now: {Student.objects.count()}")
print(f"\nClass wise student counts:")
for branch in branches:
    for year in years:
        for section in sections:
            count = Student.objects.filter(
                s_branch=branches[branch],
                s_year=years[year],
                s_section=sections[section]
            ).count()
            print(f"  {branch} Year {year} Section {section}: {count} students")
