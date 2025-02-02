"""
PDF Text Extraction Module
This module provides functionality to extract text content from PDF documents accessible via URLs.
It uses pdfplumber for PDF text extraction and handles various error cases that may occur during
the download and processing of PDF files.
The module is designed to be robust, handling network errors, malformed PDFs, and cases where
text extraction may not be possible (e.g., scanned documents).
Dependencies:
    - requests: For downloading PDF files from URLs
    - pdfplumber: For extracting text from PDF files
    - io: For handling byte streams
    - logging: For error and operation logging
    - typing: For type hints
Example:
    result = extract_pdf_text_from_url("https://example.com/sample.pdf")
    if result["success"]:
        for page in result["data"]:
            print(f"Page {page['page_number']}: {page['content']}")

"""

from typing import Dict, Union, List
import io
import logging
import requests
import pdfplumber

# Configure logging
logger = logging.getLogger(__name__)

def extract_pdf_text_from_url(pdf_url: str) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    """
    Extract text content from a PDF document accessible via URL.

    This function downloads a PDF from the given URL and extracts text content
    page by page using pdfplumber. It handles various exceptions that might
    occur during the download and extraction process.

    Args:
        pdf_url (str): The URL of the PDF document to process.

    Returns:
        Dict[str, Union[bool, str, List[Dict[str, str]]]]: A dictionary containing:
            - success (bool): Operation status (True/False)
            - message (str): Status or error message
            - data (List[Dict[str, str]]): List of dictionaries containing:
                - page_number (int): Page number
                - content (str): Extracted text content

    Raises:
        No exceptions are raised; all errors are handled and returned in the response dictionary.
    """
    response_template = {
        "success": False,
        "message": "",
        "data": []
    }

    try:
        # Fetch PDF content from URL
        response = requests.get(pdf_url, stream=True, timeout=30)
        response.raise_for_status()

        # Process PDF content
        pdf_content = io.BytesIO(response.content)
        extracted_pages = []

        with pdfplumber.open(pdf_content) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text and text.strip():
                    extracted_pages.append({
                        "page_number": page_num,
                        "content": text.strip()
                    })

        # Handle case where no text was extracted
        if not extracted_pages:
            logger.info("No text content found in PDF")
            response_template["message"] = "No text extracted. PDF may be scanned or contain only images."
            return response_template

        # Success case
        logger.info("Successfully extracted text from %d pages", len(extracted_pages))
        return {
            "success": True,
            "message": "PDF text extraction completed successfully",
            "data": extracted_pages
        }

    except requests.exceptions.RequestException as req_err:
        error_message = f"Failed to download PDF: {str(req_err)}"
        logger.error(error_message)
        response_template["message"] = error_message
        return response_template

    except pdfplumber.pdfminer.pdfparser.PDFSyntaxError as pdf_err:
        error_message = f"Invalid PDF format: {str(pdf_err)}"
        logger.error(error_message)
        response_template["message"] = error_message
        return response_template

    except (ValueError, IOError, TypeError) as err:
        error_message = f"Error during PDF processing: {str(err)}"
        logger.error(error_message)
        response_template["message"] = error_message
        return response_template
