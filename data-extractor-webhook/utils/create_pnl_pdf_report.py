"""
Module for generating and handling Profit & Loss (P&L) statement reports in PDF format.
"""

import os
import uuid
import logging
from typing import Dict, Any

from dotenv import load_dotenv
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

# pylint: disable=import-error
from utils.supabase_client import supabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_pnl_pdf_report(
    financial_data: Dict[str, Any],
    pdf_path: str,
    company_name: str = "XYZ Ltd.") -> str:
    """
    Generate a PDF report for Profit & Loss statement and upload it to Supabase storage.

    Args:
        financial_data (Dict[str, Any]): JSON data containing P&L statement information
        pdf_path (str): Path where the PDF file should be saved
        company_name (str, optional): Name of the company. Defaults to "XYZ Ltd."

    Returns:
        str: Public URL of the uploaded PDF file

    Raises:
        ValueError: If required environment variables are missing
        Exception: If file upload fails
    """
    try:
        # Initialize PDF document
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=50,
            bottomMargin=30
        )
        # Create document elements list and styles
        elements = []
        styles = _create_document_styles()

        # Add header information
        _add_document_header(elements, company_name, financial_data, styles)

        # Add financial sections
        _add_financial_sections(elements, financial_data, styles)

        # Generate PDF
        doc.build(elements)

        # Upload to Supabase
        return _upload_pdf_to_supabase(pdf_path)

    except Exception as e:
        logger.error("Failed to generate P&L report: %s", str(e))
        raise

def _create_document_styles() -> Dict[str, ParagraphStyle]:
    """Create and return document styles for the PDF report."""
    styles = getSampleStyleSheet()
    return {
        'title': ParagraphStyle(
            "TitleStyle",
            parent=styles["Title"],
            fontSize=16,
            spaceAfter=10,
            alignment=1
        ),
        'subtitle': ParagraphStyle(
            "SubtitleStyle",
            parent=styles["Normal"],
            fontSize=12,
            textColor=colors.darkblue,
            spaceAfter=6,
            alignment=1
        ),
        'bold': ParagraphStyle(
            "BoldStyle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            textColor=colors.black
        ),
        'normal': ParagraphStyle(
            "NormalStyle",
            parent=styles["Normal"],
            fontSize=10
        )
    }

def _add_document_header(elements: list,
        company_name: str,
        financial_data: Dict[str, Any],
        styles: Dict[str, ParagraphStyle]) -> None:
    """Add header information to the document elements."""
    elements.append(Paragraph(f"<b>{company_name}</b>", styles['title']))
    elements.append(Spacer(1, 15))

    report_title = f"{financial_data['period']} {financial_data['year']}"
    elements.append(Paragraph(report_title, styles['title']))
    elements.append(Paragraph(f"<b>{financial_data['currency']}</b>", styles['subtitle']))
    elements.append(Spacer(1, 10))

def _add_financial_sections(elements: list,
        financial_data: Dict[str, Any],
        styles: Dict[str, ParagraphStyle]) -> None:
    """Add financial sections to the document elements."""
    for section in financial_data["sections"]:
        elements.append(Paragraph(f"<b>{section['title']}</b>", styles['bold']))
        elements.append(Spacer(1, 5))

        table_data = _prepare_table_data(section["fields"], styles)
        table = _create_formatted_table(table_data)

        elements.append(table)
        elements.append(Spacer(1, 10))

def _prepare_table_data(fields: list, styles: Dict[str, ParagraphStyle]) -> list:
    """Prepare and format table data."""
    table_data = []
    for field in fields:
        style = styles['bold'] if field.get("bold", False) else styles['normal']
        value = _format_numeric_value(field["value"])
        table_data.append([
            Paragraph(field["label"], styles['normal']),
            Paragraph(value, style)
        ])
    return table_data

def _format_numeric_value(value: float) -> str:
    """Format numeric values with appropriate formatting."""
    if isinstance(value, (int, float)):
        return f"({abs(value):,})" if value < 0 else f"{value:,}"
    return str(value)

def _create_formatted_table(data: list) -> Table:
    """Create and style a table with the provided data."""
    table = Table(data, colWidths=[320, 120])
    table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))
    return table

def _upload_pdf_to_supabase(file_path: str) -> str:
    """
    Upload PDF file to Supabase storage.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Public URL of the uploaded file
        
    Raises:
        ValueError: If BUCKET_NAME environment variable is missing
        Exception: If upload fails
    """
    load_dotenv()
    bucket_name = os.getenv('BUCKET_NAME')
    if not bucket_name:
        raise ValueError("BUCKET_NAME environment variable is not set")

    try:
        with open(file_path, 'rb') as f:
            unique_filename = f"pl_reports/{uuid.uuid4()}.pdf"
            response = supabase.storage.from_(bucket_name).upload(
                file=f,
                path=unique_filename,
                file_options={"cache-control": "3600", "upsert": "false"}
            )

        public_url = supabase.storage.from_(bucket_name).get_public_url(response.path)
        if not public_url:
            raise ValueError("Failed to get public URL for uploaded file")

        logger.info("Successfully uploaded P&L report to Supabase: %s", unique_filename)
        return public_url

    except Exception as e:
        logger.error("Failed to upload file to Supabase: %s", str(e))
        raise
