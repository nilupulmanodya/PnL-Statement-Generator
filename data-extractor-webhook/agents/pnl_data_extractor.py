"""
Financial Data Extraction Agent

This module contains an AI agent responsible for extracting financial data from 
documents using OpenAI's GPT-4 Vision model. It processes both images and text
to generate structured financial data in JSON format.
"""

from openai import OpenAI


def pnl_data_extractor(base64_images, input_pdf_pages):
    """
    Extracts Profit and Loss (PnL) statement data from provided images and PDF text.
  This function processes financial documents to extract key financial metrics, 
  focusing on the latest quarterly data. 
  It uses OpenAI's API to analyze both image and text inputs for comprehensive data extraction.
  Args:
    base64_images (list): List of base64 encoded strings representing images of financial documents
    input_pdf_pages (str): Extracted text content from PDF pages containing financial data
  Returns:
    str: JSON formatted string containing structured financial data with the following schema:
      - period (str): Reporting period
      - year (str): Financial year
      - currency (str): Currency used
      - sections (list): Array of financial sections containing:
        - title (str): Section name
        - fields (list): Array of financial entries with:
          - label (str): Field name
          - value (float): Numerical value
          - bold (bool): Bold formatting flag
  The function follows a systematic approach to:
  1. Identify the latest quarter
  2. Validate extracted fields
  3. Enhance data completeness
  4. Format data dynamically
  5. Assign extracted values accurately
  Note:
    - Requires OpenAI API client
    - Uses GPT-4 model for processing
    - Handles both image and text inputs for comprehensive extraction
    """

    client = OpenAI()
    messages = [
        {"role": "system", "content":
         """
You are an expert in financial data extraction and validation. Your task is to accurately process
 the given financial document and extracted fields and values using a step-by-step  
 approach, ensuring that **only the latest quarterly data** is considered:

1. **Quarter Identification Phase:**
   - Extract and determine the latest quarterly period.
   - Ignore annual and outdated quarterly data.

2. **Validation Phase:**
   - Compare extracted fields with the document.
   - Identify missing fields, incorrect labels, or inconsistencies.
   - Ensure all necessary financial metrics are accounted for, including revenue, cost of 
   sales, gross profit, 
   operating expenses, finance costs, tax expenses, net profit, earnings per share, 
   and dividends per share.

3. **Enhancement Phase:**
   - Ensure correct categorization under respective sections.
   - Validate field attributes such as **bold values**, calculated sums, and subcategories.

4. **Dynamic Formatting Phase:**
   - Generate a structured JSON output, ensuring flexibility to handle different document 
   formats dynamically.
   - Maintain sections, titles, and hierarchies while allowing format changes based on 
   document variations.
   - Ensure clarity, consistency, and correct numerical representation in the final JSON output.

5. **Final Output Phase:**
   - Populate values into the structured JSON.
   - Ensure correctness in calculations and data integrity.
   - Present the final JSON output in a clean and structured manner.

Proceed step by step, following this structured approach to ensure the highest accuracy and 
completeness of extracted financial data while dynamically adapting to different formats.
"""
        },
        {"role": "user", "content": [{"type": "text", "text":f"""
Process the given financial document and extract key financial metrics specifically related to the Profit and Loss Statement for the latest quarter. Follow these steps precisely:

1. **Identify the Latest Quarter:**
   - Extract and determine the most recent quarterly data from the document.
   - Exclude any annual figures or outdated quarterly records.

2. **Validate Extracted Fields:**
   - Cross-check extracted data against the original document to ensure accuracy.
   - Identify and flag any missing, incorrect, or inconsistent fields.
   - There is posibility to have duplicate field names, add all fields accordingly.
   - Ensure to extract the currency correctly.
   - Ensure to extract the data of equity accounted investee (net of tax) correctly.

3. **Enhance Extracted Data:**
   - If relevant fields are missing or ambiguous, refine and enhance the data.
   - Ensure logical consistency and completeness across extracted information.

4. **Format Data Dynamically:**
   - Structure extracted information in a hierarchical JSON format.
   - The JSON structure should adapt dynamically to the document’s layout.
   - Include essential metadata such as:
     - Period
     - Year
     - Currency
     - Sections
     - Fields
   - Preserve formatting attributes like:
     - Titles
     - Bold values
     - Subcategories

5. **Assign Extracted Values:**
   - Populate extracted values into their respective fields.
   - Maintain numerical accuracy and ensure correct sign representation (positive/negative).
   - Represent negative values within parentheses for clarity.

6. ** Processing Considerations:**
   - You may struggle to correctly interpret embedded images.
   - Use extracted PDF text separately to ensure accurate capture of all numbers and text.
   - Structure the input clearly and consistently to improve AI’s accuracy.

**Input Section:**  {input_pdf_pages}
"""}]
        }
    ]
    # Add images correctly
    for base64_image in base64_images:
        messages.append({
            "role": "user",
            "content": [{"type": "image_url", "image_url": 
            {"url": f"data:image/jpeg;base64,{base64_image}"}}]
        })

    response_format = {
            "type": "json_schema",
            "json_schema": {
  "name": "financial_report",
  "schema": {
    "type": "object",
    "properties": {
      "period": {
        "type": "string",
        "description": "The reporting period for the financial data."
      },
      "year": {
        "type": "string",
        "description": "The year of the financial report."
      },
      "currency": {
        "type": "string",
        "description": "The currency used in the financial report."
      },
      "sections": {
        "type": "array",
        "description": "A list of sections in the financial report.",
        "items": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string",
              "description": "The title of the section."
            },
            "fields": {
              "type": "array",
              "description": "The fields within the section.",
              "items": {
                "type": "object",
                "properties": {
                  "label": {
                    "type": "string",
                    "description": "The label for the field."
                  },
                  "value": {
                    "type": "number",
                    "description": "The value associated with the label."
                  },
                  "bold": {
                    "type": "boolean",
                    "description": "Indicates if the field should be displayed in bold."
                  }
                },
                "required": [
                  "label",
                  "value",
                  "bold"
                ],
                "additionalProperties": False
              }
            }
          },
          "required": [
            "title",
            "fields"
          ],
          "additionalProperties": False
        }
      }
    },
    "required": [
      "period",
      "year",
      "currency",
      "sections"
    ],
    "additionalProperties": False
  },
  "strict": True
}

        }
    # Send the request
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format=response_format,
        max_tokens=1000,
    )
    return response.choices[0].message.content
