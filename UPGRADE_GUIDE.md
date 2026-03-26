# QR Attendance System - Upgrade Documentation

## 📋 What's New in This Version

### 1. **Database Configuration for MongoDB** ✅
- **Django is now configured to support MongoDB**
- Two configuration options provided:
  - **Local MongoDB** (`mongodb://localhost:27017/`)
  - **MongoDB Atlas** (Cloud-based, free tier available)
- Current setup uses SQLite for backward compatibility
- Easy switching between databases by uncommenting settings

### 2. **Enhanced UI** ✨
- **Modern gradient backgrounds** - Professional appearance
- **Smooth animations & transitions** - Better user experience
- **Better button styling** - Color-coded buttons (green for success, red for delete)
- **Improved header** - Added navigation link to class distribution
- **Responsive design** - Works on all screen sizes (mobile, tablet, desktop)
- **Better scrollbars** - Custom styled scrollbars matching theme
- **Shadow effects** - Depth and modern look

### 3. **Class-wise Student Distribution** 📊
- **New dedicated page**: `/class_distribution`
- **Features**:
  - View all classes in grid layout
  - Color-coded by branch (CSE, ECE, ME)
  - Statistics: Total students, total classes, average per class
  - Click any class to see detailed student list
  - View student attendance count per class

### 4. **Student Details Page** 👥
- **New page**: `/class_students/<branch_id>/<year_id>/<section_id>`
- **Shows**:
  - All students in a specific class
  - Student roll numbers and names
  - Individual attendance count
  - Professional table layout
  - Avatar badges for visual appeal

## 🚀 Getting Started

### Step 1: Install Dependencies
```powershell
cd D:\QR-Attendance-System-main
pip install -r requirements.txt
```

### Step 2: Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 3: (Optional) Repopulate Database with Sample Students
```powershell
python populate_db.py
```

### Step 4: Start Development Server
```powershell
python manage.py runserver
```

### Step 5: Access the Application
- **Main Page**: http://localhost:8000/
- **Class Distribution**: http://localhost:8000/class_distribution
- **Admin Panel**: http://localhost:8000/admin/

---

## 🗄️ Database Configuration

### Current Configuration (SQLite)
Perfect for development and testing. Data stored in `db.sqlite3`.

### Switch to MongoDB (Local)

#### Prerequisites:
1. Install MongoDB Community Edition from: https://www.mongodb.com/try/download/community
2. Ensure MongoDB service is running:
   ```powershell
   # Check if MongoDB is running
   Get-Service MongoDB
   
   # Start MongoDB if needed
   net start MongoDB
   ```

#### Configuration in `QR_Attendance_System/settings.py`:

Comment out SQLite:
```python
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
```

Uncomment MongoDB Local:
```python
DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "QR_Attendance_DB",
        "ENFORCE_SCHEMA_VALIDATION": False,
        "CLIENT": {
            "host": "mongodb://localhost:27017/",
        }
    }
}
```

Run migrations:
```powershell
python manage.py migrate
python populate_db.py
python manage.py runserver
```

### Switch to MongoDB Atlas (Cloud)

1. **Create Free Account**: https://www.mongodb.com/cloud/atlas
2. **Create Cluster**: Select M0 (free forever tier)
3. **Get Connection String**: Copy from cluster details
4. **Update settings.py**:

```python
DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "QR_Attendance_DB",
        "ENFORCE_SCHEMA_VALIDATION": False,
        "CLIENT": {
            "host": "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/QR_Attendance_DB?retryWrites=true&w=majority",
        }
    }
}
```

Replace:
- `username` - Your MongoDB Atlas username
- `password` - Your MongoDB Atlas password
- `cluster0.xxxxx` - Your cluster URL

---

## 📁 Project Structure

```
QR-Attendance-System-main/
├── FacultyView/
│   ├── views.py (UPDATED - new class distribution views)
│   ├── urls.py (UPDATED - new routes)
│   ├── models.py (Includes Attendance model with date tracking)
│   ├── templates/
│   │   ├── FacultyViewIndex.html (UPDATED UI)
│   │   ├── ClassDistribution.html (NEW)
│   │   ├── ClassStudents.html (NEW)
│   │   └── AttendanceSubmitted.html
│   ├── static/
│   │   └── FacultyView/
│   │       └── Index_Style.css (UPDATED - Enhanced styling)
│   └── templatetags/
│       ├── __init__.py (NEW)
│       └── custom_filters.py (NEW - Dictionary access filter)
├── StudentView/
│   ├── views.py (UPDATED - Database persistence)
│   └── templates/...
├── QR_Attendance_System/
│   ├── settings.py (UPDATED - MongoDB configuration)
│   └── urls.py
├── db.sqlite3 (Database)
├── MONGODB_SETUP.md (NEW - MongoDB setup guide)
├── UPGRADE_GUIDE.md (This file)
└── requirements.txt (UPDATED - Added MongoDB packages)
```

---

## 🔗 New Routes/URLs

| Route | Purpose | View |
|-------|---------|------|
| `/` | Main attendance page | faculty_view |
| `/add_manually` | Manual attendance entry | add_manually |
| `/attendance_submitted` | Success page | attendance_submitted |
| `/class_distribution` | **NEW** - Class overview | class_distribution |
| `/class_students/<branch_id>/<year_id>/<section_id>` | **NEW** - Class details | class_students |

---

## 🎨 UI Improvements

### Color Scheme
- **Primary**: #0056b3 (Professional Blue)
- **Success**: #28a745 (Green)
- **Danger**: #dc3545 (Red)
- **Background**: Linear gradient (Professional look)

### Components Updated
1. **Header** - Added navigation link to class distribution
2. **Buttons** - Gradient backgrounds, hover animations
3. **Cards** - Shadow effects, hover transformations
4. **Tables** - Alternating row colors, hover effects
5. **Forms** - Better spacing, styled select dropdowns
6. **Scrollbars** - Custom color matching theme

### Responsive Design
- Mobile: Single column layout
- Tablet: Adaptive grid
- Desktop: Full multi-column layout

---

## 📊 Sample Data

### Created Students:
- **Total**: 120 students
- **Distribution**: 
  - 3 Branches: CSE, ECE, ME
  - 4 Years: Year 1, 2, 3, 4
  - 2 Sections: A, B
  - 5 students per class

### Sample Roll Numbers
- `C1A01` - CSE Year 1 Section A Student 01
- `E2B05` - ECE Year 2 Section B Student 05
- `M3A03` - ME Year 3 Section A Student 03

---

## 🔍 Features Overview

### Attendance Page (`/`)
- ✅ QR code scanning
- ✅ Manual student addition
- ✅ Remove students from present list
- ✅ **Submit attendance button** (saves to database)
- ✅ View past attendance by date
- ✅ Link to class distribution

### Class Distribution Page (`/class_distribution`)
- ✅ View all classes in grid layout
- ✅ Statistics cards
- ✅ Branch-wise grouping
- ✅ Color-coded cards
- ✅ Click to view class details

### Class Students Page (`/class_students/...`)
- ✅ Detailed student list
- ✅ Attendance count per student
- ✅ Professional table design
- ✅ Avatar badges
- ✅ Navigation back to previous pages

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'djongo'"
**Solution**: Install packages
```powershell
pip install -r requirements.txt
```

### Issue: "Cannot connect to MongoDB"
**Solution**: Check MongoDB is running
```powershell
# Verify service
Get-Service MongoDB

# Start MongoDB
net start MongoDB

# Test connection
mongo
```

### Issue: "TemplateDoesNotExist"
**Solution**: Ensure templates exist in correct path:
- `FacultyView/templates/FacultyView/`

### Issue: "No module named 'custom_filters'"
**Solution**: Ensure templatetags module exists:
- Create `FacultyView/templatetags/__init__.py`
- Create `FacultyView/templatetags/custom_filters.py`

---

## 📝 Configuration Files

### settings.py
- Database configuration (SQLite/MongoDB options)
- INSTALLED_APPS configured
- Static files configuration

### urls.py
- New routes for class distribution
- New route for class students

### models.py
- Attendance model with date tracking
- Student, Branch, Year, Section models

### views.py
- `get_class_wise_distribution()` - Helper function
- `class_distribution()` - Class overview view
- `class_students()` - Class details view

---

## 🔐 Security Notes

- CSRF protection enabled
- Admin panel secured
- Input validation on forms
- Database queries properly handled

---

## 📚 Dependencies

```
Django 4.2+
qrcode - QR code generation
Pillow - Image processing
djongo - MongoDB ORM adapter
pymongo - MongoDB Python driver
python-dateutil - Date utilities
sqlparse - SQL parsing
```

---

## 🎓 Next Steps

1. **Deploy to Production**: Use Gunicorn + Nginx
2. **Add User Authentication**: Implement login system
3. **Export Reports**: Add PDF/Excel export functionality
4. **Mobile App**: Build native mobile app
5. **Real-time Sync**: Implement WebSocket sync
6. **Analytics Dashboard**: Add advanced reporting

---

## 💡 Tips

- Use `python manage.py createsuperuser` to create admin user
- Access admin at `/admin/`
- Backup database regularly
- For production, use environment variables for sensitive data
- Consider adding rate limiting for QR code endpoints
- Implement proper logging and error handling

---

## 📞 Support

For MongoDB setup issues, refer to: `MONGODB_SETUP.md`

For more information on Django, visit: https://docs.djangoproject.com/

---

**Version**: 2.0 with MongoDB Support & Enhanced UI  
**Last Updated**: March 26, 2026
