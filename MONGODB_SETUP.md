# MongoDB Setup Guide for QR Attendance System

## Option 1: Install MongoDB Locally (Recommended for Development)

### Windows Installation:

1. **Download MongoDB Community Edition:**
   - Visit: https://www.mongodb.com/try/download/community
   - Select Windows as Platform
   - Download the .msi installer

2. **Install MongoDB:**
   - Run the installer
   - Follow the setup wizard
   - Choose "Install MongoDB as a Service" option
   - Default installation path: `C:\Program Files\MongoDB\Server\{version}`

3. **Start MongoDB Service:**
   ```powershell
   # MongoDB should start automatically if installed as service
   # To verify it's running:
   Get-Service MongoDB
   ```

4. **Verify Installation:**
   ```powershell
   mongosh  # or mongo for older versions
   ```

---

## Option 2: Use MongoDB Atlas (Cloud-Based - No Installation)

### Setup MongoDB Atlas:

1. **Create Free Account:**
   - Visit: https://www.mongodb.com/cloud/atlas
   - Sign up for a free account
   - Create a new project

2. **Create a Cluster:**
   - Select Tier: M0 (Free Forever)
   - Choose region closest to you
   - Wait for cluster creation (5-10 minutes)

3. **Get Connection String:**
   - Click "Connect" on your cluster
   - Choose "Drivers" → Python
   - Copy the connection string
   - Format: `mongodb+srv://<username>:<password>@<cluster>.mongodb.net/`

4. **Update Django Settings:**
   After getting your connection string, update `QR_Attendance_System/settings.py`:
   
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "djongo",
           "NAME": "QR_Attendance_DB",
           "ENFORCE_SCHEMA_VALIDATION": False,
           "CLIENT": {
               "host": "mongodb+srv://username:password@cluster.mongodb.net/QR_Attendance_DB?retryWrites=true&w=majority",
           }
       }
   }
   ```

   Replace `username`, `password`, and `cluster` with your actual values.

---

## Option 3: Use Docker (Quickest Setup)

If you have Docker installed:

```powershell
# Pull and run MongoDB image
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Verify it's running
docker ps
```

Then use connection string: `mongodb://localhost:27017/`

---

## After MongoDB Setup

Run these commands:

```powershell
cd D:\QR-Attendance-System-main

# Create migrations
python manage.py makemigrations

# Migrate to MongoDB
python manage.py migrate

# Run the development server
python manage.py runserver
```

---

## Update Requirements.txt

Make sure to add MongoDB packages to requirements.txt:

```
djongo>=1.3.6
pymongo>=4.0
python-dateutil>=2.8.2
qrcode
django
pillow
```

Then install:
```powershell
pip install -r requirements.txt
```

---

## Troubleshooting

**Error: "Cannot connect to MongoDB"**
- Ensure MongoDB service is running
- Check connection string in settings.py
- For local MongoDB: verify `mongodb://localhost:27017/` is correct
- For MongoDB Atlas: verify username/password and IP whitelist

**Error: "Address already in use"**
- Kill the process on port 27017: `netstat -ano | findstr :27017`

**Performance Issues**
- Collections are automatically created by djongo
- No additional indexing needed initially
- MongoDB stores data in BSON format automatically
