#!/usr/bin/env python
"""
Script to create admin superuser account
Username: admin
Password: admin@123
Email: admin@iec.edu.in
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QR_Attendance_System.settings')
django.setup()

from django.contrib.auth.models import User

# Check if admin user already exists
if User.objects.filter(username='admin').exists():
    print("✓ Admin user already exists!")
    print("  Username: admin")
    print("  Password: admin@123 (or the password you set)")
else:
    # Create superuser
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@iec.edu.in',
        password='admin@123'
    )
    print("✓ Admin account created successfully!")
    print("\n" + "="*50)
    print("ADMIN CREDENTIALS")
    print("="*50)
    print("Username: admin")
    print("Password: admin@123")
    print("Email: admin@iec.edu.in")
    print("="*50)
    print("\nAccess admin panel at: http://localhost:8000/admin/")
    print("="*50)
