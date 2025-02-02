"""
Webhook listener for processing CSE reports and generating PnL statements.
This module handles incoming webhooks, processes PDF reports, and updates the database with results.
"""

import json
import logging
from typing import Tuple

from flask import Flask, request, jsonify
from flask.wrappers import Response

from utils.extract_pdf_text_from_url import extract_pdf_text_from_url
from utils.extract_page_images_from_pdf import extract_page_images_from_pdf
from utils.create_pnl_pdf_report import create_pnl_pdf_report
# pylint: disable=import-error
from utils.supabase_client import supabase

from agents.extract_consolidated_income_statement import extract_consolidated_income_statement
from agents.pnl_data_extractor import pnl_data_extractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def update_record_status(record_id: str, status: str, pl_report_url: str = None) -> None:
    """
    Update the status and PL report URL in the database.
    
    Args:
        record_id (str): The record identifier
        status (str): Status to update ('success' or 'error')
        pl_report_url (str, optional): URL of the generated PL report
    """
    try:
        update_data = {'status': status}
        if pl_report_url:
            update_data['pl_report'] = pl_report_url

        supabase.table('table').update(update_data).eq('id', record_id).execute()
    except (ValueError, TypeError, ConnectionError) as e:
        logger.error("Failed to update record status: %s", e)

@app.route('/webhook', methods=['POST'])
def process_cse_report() -> Tuple[Response, int]:
    """
    Process incoming CSE reports and generate PnL statements.
    
    Returns:
        tuple: JSON response and HTTP status code
    """
    try:
        webhook_data = request.json
        record_id = webhook_data['record']['id']
        cse_report_url = webhook_data['record']['cse_report']

        logger.info("Processing CSE report for record ID: %s", record_id)

        # Extract PDF text
        pdf_text_result = extract_pdf_text_from_url(cse_report_url)

        # Process consolidated income statement
        relevant_pages = json.loads(extract_consolidated_income_statement(pdf_text_result))

        if not relevant_pages or relevant_pages.get("status") != "relevant":
            logger.info("No relevant pages found for record ID: %s", record_id)
            update_record_status(record_id, 'error')
            return jsonify({"status": "not_relevant", "message": "No relevant pages found"}), 200

        # Extract images from relevant pages
        page_numbers = relevant_pages.get("page_numbers")
        company_name = relevant_pages.get("company_name")

        consolidate_statement_snapshots = extract_page_images_from_pdf(
            cse_report_url,
            page_numbers
        )

        # Extract relevant content
        extracted_content = [
            item["content"] for item in pdf_text_result['data']
            if item["page_number"] in page_numbers
        ]

        # Generate final report
        final_data = json.loads(pnl_data_extractor(
            consolidate_statement_snapshots,
            extracted_content
        ))

        report_filename = "output-report.pdf"
        uploaded_url = create_pnl_pdf_report(
            final_data,
            report_filename,
            company_name
        )

        # Update record with success status
        update_record_status(record_id, 'success', uploaded_url)

        return jsonify({
            "status": "success",
            "message": "PnL report generated successfully"
        }), 200

    except (json.JSONDecodeError, ValueError, IOError, ConnectionError) as e:
        logger.error("Error processing webhook: %s", str(e))
        if 'record_id' in locals():
            update_record_status(record_id, 'error')
        return jsonify({
            "status": "error",
            "message": "Failed to process report"
        }), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
