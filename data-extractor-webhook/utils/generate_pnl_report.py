from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import json
from utils.supabase_client import supabase
import uuid

def generate_pnl_report(json_data, output_pdf, company_name="XYZ Ltd."):
    doc = SimpleDocTemplate(output_pdf, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=50, bottomMargin=30)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=16, spaceAfter=10, alignment=1)
    subtitle_style = ParagraphStyle("SubtitleStyle", parent=styles["Normal"], fontSize=12, textColor=colors.darkblue, spaceAfter=6, alignment=1)
    bold_style = ParagraphStyle("BoldStyle", parent=styles["Normal"], fontName="Helvetica-Bold", textColor=colors.black)
    normal_style = ParagraphStyle("NormalStyle", parent=styles["Normal"], fontSize=10)

    # Add company name
    elements.append(Paragraph(f"<b>{company_name}</b>", title_style))
    elements.append(Spacer(1, 15))

    # Add Report Title
    report_title = f"{json_data['period']} {json_data['year']}"
    elements.append(Paragraph(report_title, title_style))
    elements.append(Paragraph(f"<b>{json_data['currency']}</b>", subtitle_style))
    elements.append(Spacer(1, 10))

    for section in json_data["sections"]:
        elements.append(Paragraph(f"<b>{section['title']}</b>", bold_style))
        elements.append(Spacer(1, 5))

        data = []
        for field in section["fields"]:
            style = bold_style if field.get("bold", False) else normal_style
            value = f"{field['value']:,}"  # Formatting numbers with commas
            if isinstance(field["value"], (int, float)) and field["value"] < 0:
                value = f"({abs(field['value']):,})"  # Negative values in brackets
            
            data.append([Paragraph(field["label"], normal_style), Paragraph(value, style)])

        # Create a table
        table = Table(data, colWidths=[320, 120])
        table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke if len(data) % 2 == 0 else colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
        ]))

        elements.append(table)
        elements.append(Spacer(1, 10))  # Space between sections

    # Build PDF
    doc.build(elements)

    def upload_to_supabase(file_path, bucket_name):


        with open(file_path, 'rb') as f:
            unique_filename = f"pl_reports/{uuid.uuid4()}.pdf"
            response = supabase.storage.from_(bucket_name).upload(
                file=f,
                path=unique_filename,
                file_options={"cache-control": "3600", "upsert": "false"},
            )

        print("response", response)

        uploaded_url = supabase.storage.from_(bucket_name).get_public_url(
            response.path
        )
        print("uploaded_url", uploaded_url)
        if uploaded_url:
            return uploaded_url
        else:
            raise Exception("Failed to upload file to Supabase")

    bucket_name = "project_pl_generation" # TODO

    file_url = upload_to_supabase(output_pdf, bucket_name)
    return file_url
