from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from glaucoma_detection.models import DetectionResult
from datetime import datetime

def download_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="glaucoma_report.pdf"'

    case_id = request.GET.get('case')
    
    if case_id:
        try:
            result = get_object_or_404(DetectionResult, id=case_id)
        except:
            result = None
    else:
        result = None

    # Create canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 50, "GLAUCOMA SCREENING REPORT")
    
    # Separator line
    p.setStrokeColorRGB(0.2, 0.2, 0.2)
    p.line(50, height - 65, width - 50, height - 65)
    
    # Report date
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 85, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Patient Information Section
    if result:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, height - 115, "PATIENT INFORMATION")
        
        p.setFont("Helvetica", 10)
        y_pos = height - 140
        
        if result.patient_id:
            p.drawString(50, y_pos, f"Patient ID: {result.patient_id}")
            y_pos -= 20
        
        if result.patient_name:
            p.drawString(50, y_pos, f"Patient Name: {result.patient_name}")
            y_pos -= 20
        
        if result.patient_age:
            p.drawString(50, y_pos, f"Patient Age: {result.patient_age} years")
            y_pos -= 20
        
        p.drawString(50, y_pos, f"Examined By: Dr. {result.user.get_full_name() or result.user.username}")
        y_pos -= 30
        
        # Separator line
        p.setStrokeColorRGB(0.2, 0.2, 0.2)
        p.line(50, y_pos, width - 50, y_pos)
        
        # Screening Results Section
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_pos - 25, "SCREENING RESULTS")
        
        p.setFont("Helvetica", 10)
        y_pos -= 50
        
        # Result with color coding
        result_color = (0.8, 0.2, 0.2) if result.prediction == "Glaucoma" else (0.2, 0.6, 0.2)
        p.setFillColorRGB(*result_color)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_pos, f"DIAGNOSIS: {result.prediction.upper()}")
        
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 10)
        y_pos -= 25
        
        p.drawString(50, y_pos, f"Confidence Score: {result.confidence:.2f}%")
        y_pos -= 20
        
        p.drawString(50, y_pos, f"Probability (Raw): {result.probability:.4f}")
        y_pos -= 30
        
        # Interpretation
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y_pos, "INTERPRETATION:")
        
        p.setFont("Helvetica", 9)
        y_pos -= 20
        
        if result.prediction == "Glaucoma":
            interpretation = "The AI system has detected glaucomatous features in the fundus image. Immediate ophthalmologic consultation is recommended for further evaluation and treatment."
            color = (0.8, 0.2, 0.2)
        else:
            interpretation = "The fundus image appears normal with no significant glaucomatous features detected. Routine follow-up is recommended per standard care guidelines."
            color = (0.2, 0.6, 0.2)
        
        p.setFillColorRGB(*color)
        text_lines = []
        words = interpretation.split()
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= 80:
                current_line += word + " "
            else:
                text_lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            text_lines.append(current_line.strip())
        
        for line in text_lines:
            p.drawString(50, y_pos, line)
            y_pos -= 15
        
        y_pos -= 20
        
        # Scan date
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 9)
        p.drawString(50, y_pos, f"Scan Date & Time: {result.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
    else:
        # Fallback if case not found
        case_id = request.GET.get('case', 'N/A')
        result_text = request.GET.get('result', 'N/A')
        prob = request.GET.get('prob', '0')
        doctor = request.user.username if getattr(request, 'user', None) and request.user.is_authenticated else 'N/A'
        
        p.setFont("Helvetica", 10)
        p.drawString(50, height - 120, f"Case ID: {case_id}")
        p.drawString(50, height - 140, f"Result: {result_text}")
        p.drawString(50, height - 160, f"Confidence: {prob}%")
        p.drawString(50, height - 180, f"Doctor: {doctor}")
    
    # Footer
    p.setFont("Helvetica", 8)
    p.setFillColorRGB(0.5, 0.5, 0.5)
    p.drawString(50, 30, "This report is generated by an AI-based glaucoma detection system.")
    p.drawString(50, 20, "Results should be reviewed by a qualified ophthalmologist. This is not a diagnostic tool replacement.")

    p.showPage()
    p.save()
    return response
