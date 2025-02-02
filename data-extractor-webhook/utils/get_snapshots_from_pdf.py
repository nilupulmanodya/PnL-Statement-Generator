import requests
import base64
import io
from typing import List
from pdf2image import convert_from_bytes
import os

def get_snapshots_from_pdf(pdf_url: str, page_numbers: List[int]) -> List[str]:
    """
    Extract images from specific pages of a PDF and return them as base64 encoded strings.
    
    Args:
        pdf_url (str): URL of the PDF file
        page_numbers (List[int]): List of page numbers to extract (1-based indexing)
    
    Returns:
        List[str]: List of base64 encoded strings of the page images
    """
    try:
        # Download PDF from URL
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Convert PDF pages to images
        images = convert_from_bytes(
            response.content,
            dpi=800,  # Higher DPI for better quality
        )

        base64_images = []
        save_dir = './base64_images'
        os.makedirs(save_dir, exist_ok=True)

        for page_num in page_numbers:
            if page_num < 1 or page_num > len(images):
                raise ValueError(f"Page number {page_num} is out of range")

            # Convert selected pages to base64
            img = images[page_num - 1]  # 1-based index to 0-based

            # Save image to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            # Convert to base64
            base64_image = base64.b64encode(img_byte_arr).decode()
            base64_images.append(base64_image)

            # Save image as file
            file_path = os.path.join(save_dir, f'page_{page_num}.jpg')
            with open(file_path, 'wb') as f:
                f.write(img_byte_arr)  # Correctly save the binary image

        return base64_images

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error downloading PDF: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")
