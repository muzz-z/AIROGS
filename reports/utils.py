from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_report(patient_result):
    file_name = f"glaucoma_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join("media/reports", file_name)

    os.makedirs("media/reports", exist_ok=True)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "AI-Based Glaucoma Screening Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Prediction : {patient_result['prediction']}")
    c.drawString(50, height - 130, f"Confidence : {patient_result['confidence']}%")
    c.drawString(50, height - 160, f"Probability : {patient_result['raw_prob']}")
    c.drawString(50, height - 190, f"Date       : {datetime.now().strftime('%d-%m-%Y %H:%M')}")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(
        50,
        100,
        "Note: This report is AI-assisted and should be confirmed by an ophthalmologist."
    )

    c.save()
    return file_path
