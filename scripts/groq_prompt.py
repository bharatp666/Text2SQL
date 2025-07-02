import requests
import json
import os
from datetime import datetime

# with open("llama_prompt.txt", "r") as f:
#     prompt_text = f.read()

# GROQ_API_KEY = "<YOUR_GROQ_API_KEY>"
# MODEL = "llama3-8b-8192"

# url = "https://api.groq.com/openai/v1/chat/completions"
# headers = {
#     "Authorization": f"Bearer {GROQ_API_KEY}",
#     "Content-Type": "application/json"
# }

# data = {
#     "model": MODEL,
#     "messages": [
#         {"role": "system", "content": "You are a helpful assistant that generates SQL queries for BigQuery."},
#         {"role": "user", "content": prompt_text}
#     ],
#     "temperature": 0.2
# }

# response = requests.post(url, headers=headers, data=json.dumps(data))

# if response.status_code == 200:
#     print("\n--- Generated SQL ---\n")
#     print(response.json()["choices"][0]["message"]["content"])
# else:
#     print("Error:", response.status_code)
#     print(response.text)


# -- Configuration -- #
MODEL = "llama3-8b-8192"
PROMPT_FILE = "llama_prompt.txt"
OUTPUT_DIR = "../outputs"

# -- Checking if the outout directory exists -- #
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Step 1: Read the prompt from file --- #
with open(PROMPT_FILE, "r") as f:
    prompt_text = f.read()

# --- Step 2: Define API call parameters --- #
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

prompt = (
    "You are a helpful assistant that generates BigQuery-compliant SQL queries. "
    "Explicitly mention the dataset_id along with table names in your queries. "
    "Utilize the best practices as given below:\n\n"
    "1. Avoid SELECT * — only include the necessary columns.\n"
    "2. Use table aliases for clarity and brevity.\n"
    "3. Use appropriate JOIN types (INNER, LEFT, etc.) based on the logical relationship.\n"
    "4. Apply WHERE filters early to reduce data scanned.\n"
    "5. Use indexed columns in WHERE and JOIN clauses when applicable.\n"
    "6. Avoid unnecessary CTEs or subqueries if a direct query is more efficient.\n"
    "7. Include ORDER BY and LIMIT only if needed by the use case.\n"
    "8. Use DISTINCT only if:\n"
    "   - The result should include unique rows (e.g., unique customers, products, IDs), especially when joining with one-to-many relationships like orders, order_items, etc.\n"
    "   - The business requirement implies uniqueness — such as 'list of customers,' 'distinct products sold,' or 'unique users.'\n"
    "   - The selected columns are not guaranteed to be unique due to the JOIN condition.\n\n"
    "***The query output format should be a Python inline string (triple quotes) so that it is directly consumable, and only the SQL query should be returned without any explanations.***"
)

data = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": prompt},
        {"role": "user", "content": prompt_text}
    ],
    "temperature": 0,
    "top_p":0
}

# --- Step 3: Make the API call --- #
response = requests.post(url, headers=headers, data=json.dumps(data))

# --- Step 4: Handle the response --- #
if response.status_code == 200:
    reply = response.json()["choices"][0]["message"]["content"]
    print("\n--- Generated SQL ---\n")
    print(reply)

    # Save to ../outputs/sql_response_<timestamp>.txt
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"sql_response_{timestamp}.txt")

    with open(output_path, "w") as out_file:
        out_file.write(reply)

    print(f"\n Response saved to: {output_path}")
else:
    print("Error:", response.status_code)
    print(response.text)