"""
Module for extracting and converting pages from PDF files into base64 encoded images.
This module provides functionality to:
- Download PDFs from URLs
- Convert specific PDF pages to high-quality images
- Save extracted images locally
- Convert images to base64 encoded strings
The main functionality is provided through the extract_page_images_from_pdf function,
which handles the entire workflow from PDF download to image extraction and encoding.
Functions:
    extract_page_images_from_pdf: Extracts specified pages from a PDF and 
    converts them to base64 encoded images
Classes:
    PDFProcessingError: Custom exception for handling PDF processing failures
Dependencies:
    - pdf2image: For PDF to image conversion
    - requests: For downloading PDFs from URLs
    - pathlib: For file system operations
    - base64: For image encoding
    - logging: For operation logging
"""

from typing import List, Optional
import io
import base64
import logging
from pathlib import Path

import requests
from pdf2image import convert_from_bytes
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessingError(Exception):
    """Custom exception for PDF processing errors."""

def extract_page_images_from_pdf(
    pdf_url: str,
    target_pages: List[int],
    output_dir: str = './extracted_images',
    image_dpi: int = 800
) -> Optional[List[str]]:
    """
    Extract and convert specific pages from a PDF into base64 encoded images.
    
    This function performs the following steps:
    1. Downloads a PDF from the provided URL
    2. Converts specified pages to high-quality images
    3. Saves the images locally
    4. Returns base64 encoded strings of the images
    
    Args:
        pdf_url (str): The URL of the PDF file to process
        target_pages (List[int]): List of page numbers to extract (1-based indexing)
        output_dir (str): Directory path to save the extracted images
        image_dpi (int): DPI resolution for the extracted images
    
    Returns:
        Optional[List[str]]: List of base64 encoded strings of the page images
                            Returns None if processing fails
    
    Raises:
        PDFProcessingError: If there's an error during PDF processing
        ValueError: If provided page numbers are invalid
    """
    try:
        # Validate input parameters
        if not target_pages:
            raise ValueError("No target pages provided")
        if not pdf_url:
            raise ValueError("PDF URL cannot be empty")

        # Create output directory using pathlib
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Download PDF
        logger.info("Downloading PDF from: %s", pdf_url)
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()

        # Convert PDF to images
        logger.info("Converting PDF pages to images")
        pdf_images = convert_from_bytes(
            response.content,
            dpi=image_dpi,
        )

        # Validate page numbers
        max_pages = len(pdf_images)
        invalid_pages = [p for p in target_pages if p < 1 or p > max_pages]
        if invalid_pages:
            raise ValueError(
                f"Invalid page numbers: {invalid_pages}. "
                f"PDF has {max_pages} pages"
            )

        # Process each requested page
        base64_encoded_images = []
        for page_num in target_pages:
            logger.info("Processing page %d", page_num)

            # Get image for the current page (convert 1-based to 0-based index)
            current_image = pdf_images[page_num - 1]

            # Convert image to bytes
            image_buffer = io.BytesIO()
            current_image.save(image_buffer, format='JPEG')
            image_bytes = image_buffer.getvalue()

            # # Save image to file
            # image_path = output_path / f'page_{page_num}.jpg'
            # image_path.write_bytes(image_bytes)

            # Convert to base64
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            base64_encoded_images.append(base64_image)

        logger.info("Successfully processed %d pages", len(target_pages))
        return base64_encoded_images

    except RequestException as e:
        logger.error("Failed to download PDF: %s", e)
        raise PDFProcessingError(f"PDF download failed: {str(e)}") from e
    except ValueError as e:
        logger.error("Invalid input parameters: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error during PDF processing: %s", e)
        raise PDFProcessingError(f"PDF processing failed: {str(e)}") from e
