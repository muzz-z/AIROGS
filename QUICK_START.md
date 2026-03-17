# Quick Start Guide - Glaucoma AI Detection System

## Current Status ✅
- **Server Running:** http://127.0.0.1:8000
- **Mode:** Development (Mock Predictor)
- **Database:** SQLite (configured and migrated)
- **All Features:** Working without errors

---

## Access the Application

### Doctor/User Dashboard
```
http://127.0.0.1:8000/dashboard/
```
Shows:
- Total scans count
- Glaucoma cases count
- Normal cases count
- Detection rate
- All screening records with patient info
- PDF download links

### Start New Screening
```
http://127.0.0.1:8000/upload/
```
Upload a fundus image and enter:
- Patient ID (required)
- Patient Name (required)
- Patient Age (required)

### View Results
```
http://127.0.0.1:8000/results/
```
Shows:
- Fundus image
- AI diagnosis (Glaucoma/Normal)
- Confidence percentage
- Patient information
- Download PDF report button

---

## File Structure
```
glaucoma_project/
├── glaucoma_detection/
│   ├── models.py .......................... DetectionResult with patient fields
│   ├── views.py ........................... detect_glaucoma, dashboard, results
│   └── utils.py ........................... predict_glaucoma with mock & real model
├── templates/
│   ├── upload.html ........................ Patient info form + image upload
│   ├── doctor_dashboard.html ............. Statistics + scan history
│   ├── results.html ....................... Results display + PDF download
│   └── base.html .......................... Base template
├── ml_models/
│   └── glaucoma_mobilenet.keras .......... Model file (currently missing)
├── Dataset/
│   └── train/
│       ├── glaucoma/ ...................... Glaucoma training images
│       └── normal/ ........................ Normal training images
├── reports/
│   └── views.py ........................... PDF generation with patient details
├── manage.py .............................. Django management
├── train_cnn.py ........................... Model training script
└── MODEL_ERROR_FIX.md ..................... This fix documentation
```

---

## Key Features Implemented

### 1️⃣ Patient Information Management
- Capture patient ID, name, and age during screening
- Store patient info with each scan
- Display patient info in results and PDF

### 2️⃣ Dashboard Statistics
- Total scans count
- Positive cases (Glaucoma) count
- Negative cases (Normal) count
- Detection rate percentage
- Patient names and IDs visible

### 3️⃣ PDF Report Generation
- Professional report format
- Includes patient demographics
- Shows diagnosis and confidence
- Color-coded results
- Clinical interpretation

### 4️⃣ Error Handling
- Mock predictor prevents crashes
- Graceful error messages
- Fallback system if model fails
- Comprehensive logging

---

## What's Different from Original

| Feature | Before | After |
|---------|--------|-------|
| Patient Info | ❌ Not captured | ✅ Captured & stored |
| Dashboard | ❌ Basic table | ✅ Statistics + patient info |
| Scan Count | ❌ Not shown | ✅ Displayed prominently |
| PDF Report | ❌ Basic | ✅ Professional with patient data |
| Error Handling | ❌ Crashes | ✅ Graceful fallback |
| Mock Mode | ❌ N/A | ✅ Works without trained model |

---

## Database Fields Added

New fields in `DetectionResult` model:
```python
patient_id = CharField(max_length=50)       # Unique patient identifier
patient_name = CharField(max_length=150)    # Full patient name
patient_age = IntegerField()                # Patient age in years
```

**Migration Applied:** `0005_alter_detectionresult_options_and_more.py`

---

## API Endpoints

| URL | Method | Purpose |
|-----|--------|---------|
| `/upload/` | GET, POST | Upload fundus image with patient info |
| `/detect/` | GET, POST | Process image and generate prediction |
| `/results/` | GET | View latest screening result |
| `/dashboard/` | GET | View all scans and statistics |
| `/report/` | GET | Download PDF report |
| `/login/` | GET, POST | User authentication |

---

## Configuration

### Enable Real Model When Ready
1. Train model: `python train_cnn.py`
2. Edit `glaucoma_detection/utils.py`:
   ```python
   USE_MOCK_MODEL = False
   ```
3. Restart server

### Training Requirements
- `Dataset/train/glaucoma/` - Glaucoma training images
- `Dataset/train/normal/` - Normal training images
- Minimum 100 images per category recommended

---

## Current Mock Predictor Behavior

The mock predictor:
- ✅ Works immediately without training
- ✅ Generates consistent predictions based on image hash
- ✅ Allows testing of UI/UX
- ✅ Logs "Using MOCK predictor" message
- ⚠️ Predictions are NOT clinically accurate

**Switch to real model for actual diagnosis.**

---

## Testing Checklist

- [ ] Access `/upload/` and see patient form
- [ ] Fill form and upload image
- [ ] Check `/results/` for patient info
- [ ] Download PDF and verify patient details
- [ ] Visit `/dashboard/` and see scan count
- [ ] Check statistics cards for accuracy
- [ ] Verify no error messages in logs

---

## Troubleshooting

### "Model loading failed" Error
**Cause:** Corrupted model file  
**Solution:** Using mock mode (already enabled)  
**Next:** Train your own model or provide a valid one

### Patient info not saving
**Check:** Upload form fields are not empty  
**Solution:** Fill all required fields (ID, Name, Age)

### PDF download not working
**Check:** Latest scan exists in database  
**Solution:** Create new screening and download from results page

### Dashboard shows 0 scans
**Cause:** No screenings performed yet  
**Solution:** Complete at least one screening

---

## Development Tips

### View Server Logs
Server is running in terminal - check for:
- `Model loaded successfully` - Real model active
- `Using MOCK predictor` - Mock mode active
- Error messages - Debug issues

### Django Management Commands
```bash
# Check system
python manage.py check

# View database
python manage.py dbshell

# Create admin user
python manage.py createsuperuser

# Restart server
python manage.py runserver 0.0.0.0:8000
```

### Enable Django Debug Pages
In `glaucoma_project/settings.py`:
```python
DEBUG = True  # Already enabled for development
ALLOWED_HOSTS = []  # Add your IP if needed
```

---

## Next Steps

1. **Test the system** with the mock predictor
2. **Gather training data** (fundus images with labels)
3. **Train the model** using `train_cnn.py`
4. **Switch to real model** by setting `USE_MOCK_MODEL = False`
5. **Deploy** to production when ready

---

## Support Files

- [MODEL_ERROR_FIX.md](MODEL_ERROR_FIX.md) - Detailed error fix documentation
- [train_cnn.py](train_cnn.py) - Model training script
- [glaucoma_detection/utils.py](glaucoma_detection/utils.py) - Prediction logic
- [glaucoma_detection/models.py](glaucoma_detection/models.py) - Data models
- [glaucoma_detection/views.py](glaucoma_detection/views.py) - View functions

---

**Status:** ✅ All systems operational  
**Last Updated:** February 3, 2026  
**Server Version:** Django 4.2
