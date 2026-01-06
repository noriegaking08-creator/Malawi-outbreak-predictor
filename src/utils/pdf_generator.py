from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime

def generate_pdf(pred_df):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Malawi Outbreak Predictor Report")
    c.drawString(100, 730, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = 700
    for _, row in pred_df.iterrows():
        c.drawString(100, y, f"{row['district']}: {row['predicted_cases']:.0f} cases ({row['disease']}), Risk: {row['risk']}")
        y -= 20
    c.save()
    buffer.seek(0)
    return buffer