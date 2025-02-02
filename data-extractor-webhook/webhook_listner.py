import os

from flask import Flask, request, jsonify

from utils.get_pdf_text_from_url import get_pdf_text_from_url
from utils.get_snapshots_from_pdf import get_snapshots_from_pdf
from utils.generate_pnl_report import generate_pnl_report
from agents.data_extractor import data_extractor
from agents.fin_data_extractor import fin_data_extractor
from utils.supabase_client import supabase
import json


app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    cse_report_url = data['record']['cse_report']
    print("New Record:", data)
    print("cse_report_url", cse_report_url)

    # Extract text from the PDF URL
    result = get_pdf_text_from_url(cse_report_url)
    # print(result['data'][0])
    try:
        relevant_pages = fin_data_extractor(result)
        # relevant_pages = {"page_numbers": [3], "status": "relevant"}
        relevant_pages = json.loads(relevant_pages)
        if relevant_pages and relevant_pages.get("status") == "relevant":
            print("relevant_pages", relevant_pages)
            consolidate_statement_snapshots = get_snapshots_from_pdf(cse_report_url, relevant_pages.get("page_numbers"))
            
            # fields = fields_extractor(consolidate_statement_snapshots)
            extracted_content = [
                item["content"] for item in result['data'] if item["page_number"] in relevant_pages["page_numbers"]
            ]

            print('extracted_content>>>>>>>>>>>>>>>',extracted_content)

            final_json = json.loads(data_extractor(consolidate_statement_snapshots, extracted_content))
            

            print("Final JSON:", final_json)
            uploaded_url = generate_pnl_report(final_json,"output-report.pdf",relevant_pages.get("company_name"))


            # Update the table with the URL for pl_report
            update_response = supabase.table('table').update({'pl_report': uploaded_url, 'status': 'success'}).eq('id',data['record']['id']).execute()
            print("Update Response:", update_response)

            return jsonify({"page_numbers": [], "status": "relevant"}), 200
        else:
            print("Not relevant")
            return jsonify({"page_numbers": [], "status": "not relevant"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"page_numbers": [], "status": "not relevant"}), 200
    # os.system("python your_script.py")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
