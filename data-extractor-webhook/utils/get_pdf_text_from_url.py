import requests
import io
import pdfplumber
from typing import Dict, Union, List

def get_pdf_text_from_url(pdf_url: str) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    """
    Download a PDF from a URL and extract text page by page.

    Args:
        pdf_url (str): URL of the PDF document.

    Returns:
        Dict containing:
            - success (bool): Whether the operation was successful.
            - message (str): Success/error message.
            - data (List[Dict[str, str]]): Page number to text mapping.
    """
    try:
        # Download PDF from URL
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()  # Raise exception for bad status codes

        # Create PDF reader object
        pdf_file = io.BytesIO(response.content)
        result = []

        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    result.append({
                        "page_number": page_num,
                        "content": text.strip()
                    })
        
        if not result:
            return {
                "success": False,
                "message": "No text extracted. The PDF might be scanned or have embedded images.",
                "data": []
            }

        return {
            "success": True,
            "message": "PDF text extracted successfully",
            "data": result
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Failed to download PDF: {str(e)}",
            "data": []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}",
            "data": []
        }

# Test with your PDF URL
# pdf_url = "https://khucoxrjdvrgifuegqoc.supabase.co/storage/v1/object/public/project_pl_generation/cse_reports/670_1731321532619.pdf"
# pdf_url = "https://khucoxrjdvrgifuegqoc.supabase.co/storage/v1/object/public/project_pl_generation/cse_reports/771_1730893408597.pdf"
# pdf_url = "https://khucoxrjdvrgifuegqoc.supabase.co/storage/v1/object/public/project_pl_generation/cse_reports/2.pdf"
# result = get_pdf_text_from_url(pdf_url)
# print(result)
