from openai import OpenAI


def fin_data_extractor(cse_report):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": """You are an AI assistant specialized in processing financial reports. 
                Your task is to extract the pages that contain the consolidated income statement 
                (i.e. the statement of profit or loss for the group) rather than the company-specific 
                statements. 
                Do the following:
                - Identify pages where the content includes titles such as "STATEMENT OF PROFIT OR LOSS" 
                    with group-level data (for example, if the header shows “Group” or similar indications).
                - Do NOT return pages that include "Company Statement of Financial Position", "
                    Company Income Statements", "Statements of Comprehensive Income", "Statements of Changes 
                    in Equity", "Cash Flow Statements", "Notes to the Financial Statements", "Shareholder 
                    Information", or any similar sections.
                - If the consolidated data spans multiple pages, return all such pages.
                - Return the page numbers and their content.
                If any content that is not related to the financial report is accidentally pasted, respond 
                with an error message indicating that the content is not related.

                Remember, your goal is to help extract only the consolidated (group) profit 
                and loss data. not consolidate (company)"""},
        {"role": "user", "content": f"""I have a JSON document where each item is a page from a CSE report. I need 
                        to extract the pages that contain the consolidated income statement – 
                        specifically the “STATEMENT OF PROFIT OR LOSS” for the group (i.e. not 
                        the “Company” ones). For example, I am interested in sections titled 
                        like "STATEMENT OF PROFIT OR LOSS" that show group data (e.g., “Group”) 
                        or are labeled as “Consolidated Income Statements.” Please process the JSON 
                        and return only the pages that meet this criteria.  I only need the page number(s) 
                        that contain that data. If I accidentally paste any content that is not related to 
                        the report, please respond with an error message. 

                        Here is the JSON document: 

                        {cse_report}

                        Please return only the company name and the page number(s) that contain the valid quarterly (3‑month) 
                        data from the latest year."""
        
        }
    ],
    response_format={
            "type": "json_schema",
            "json_schema": {
  "name": "page_numbers_status",
  "schema": {
    "type": "object",
    "properties": {
      "page_numbers": {
        "type": "array",
        "description": "A list of page numbers.",
        "items": {
          "type": "number"
        }
      },
      "status": {
        "type": "string",
        "description": "Indicates the relevance of the document",
        "enum": [
          "relevant",
          "not relevant"
        ]
      },
      "company_name": {
        "type": "string",
        "description": "The name of the company associated with the document."
      }
    },
    "required": [
      "page_numbers",
      "status",
      "company_name"
    ],
    "additionalProperties": False
  },
  "strict": True
},
        },


    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
    return {"page_numbers": [3], "status": "relevant"}

