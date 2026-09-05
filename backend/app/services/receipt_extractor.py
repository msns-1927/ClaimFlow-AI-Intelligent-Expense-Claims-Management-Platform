import json

from groq import Groq

from app.database.session import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


EXTRACTION_PROMPT = """
You extract expense information from raw receipt text.

The receipt text may be:
- badly formatted
- abbreviated
- misspelled
- missing labels
- copied manually by a user
- written in different date formats

Extract the expense information supported by the receipt.

Important rules:

1. Do not invent information that is not supported by the receipt.
2. Convert the expense date to YYYY-MM-DD.
3. Extract the final transaction amount.
4. If the receipt indicates Indian rupees, use INR.
5. Choose exactly one of these categories:
   TRAVEL
   MEALS
   ACCOMMODATION
   OFFICE_SUPPLIES
   TAXI_LOCAL_TRANSPORT
   CLIENT_EXPENSE
   OTHER
6. Keep the merchant name understandable even when the receipt is abbreviated.
7. Write a concise description of the expense.
8. Confidence must be between 0 and 1.
"""


RECEIPT_SCHEMA = {
    "type": "object",
    "properties": {
        "merchant": {
            "type": "string"
        },
        "expense_date": {
            "type": "string"
        },
        "amount": {
            "type": "number"
        },
        "currency": {
            "type": "string"
        },
        "category": {
            "type": "string",
            "enum": [
                "TRAVEL",
                "MEALS",
                "ACCOMMODATION",
                "OFFICE_SUPPLIES",
                "TAXI_LOCAL_TRANSPORT",
                "CLIENT_EXPENSE",
                "OTHER"
            ]
        },
        "description": {
            "type": "string"
        },
        "confidence": {
            "type": "number"
        }
    },
    "required": [
        "merchant",
        "expense_date",
        "amount",
        "currency",
        "category",
        "description",
        "confidence"
    ],
    "additionalProperties": False
}


def extract_receipt_data(raw_text: str) -> dict:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": EXTRACTION_PROMPT,
            },
            {
                "role": "user",
                "content": raw_text,
            },
        ],
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "expense_receipt",
                "strict": True,
                "schema": RECEIPT_SCHEMA,
            },
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty response")

    return json.loads(content)