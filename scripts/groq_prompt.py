import requests
import json
import os
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration --- #
GROQ_API_KEY = "<Groq API Key"  
MODEL = "llama3-8b-8192"
PROMPT_FILE = "llama_prompt.txt"
OUTPUT_DIR = "../outputs"
PROJECT_ID = "<Project ID>"  
CREDENTIALS_FILE = "<path_to_your_service_account_key.json>"  

# --- Ensure output directory exists --- #
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Step 1: Read the prompt --- #
with open(PROMPT_FILE, "r") as f:
    prompt_text = f.read()

# --- Step 2: Get SQL from Groq --- #
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
data = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": (
                            "You are a senior data analyst who writes optimized and cost-efficient SQL queries for Google BigQuery.\n\n"
      "Guidelines:\n"
                            "1. Always qualify table names using the dataset_id (e.g., `retail.orders`)\n"
                            "2. Avoid SELECT * — return only the necessary columns\n"
                            "3. Use EXISTS or semi-joins instead of JOINs when only checking for row existence\n"
                            "4. Write queries that minimize data scanned to reduce cost\n"
                            "5. Add filters on partitioned columns (e.g., order_date) early in the WHERE clause\n"
                            "6. Return only the raw BigQuery-compliant SQL with no markdown or explanation"
  )
},
        {"role": "user", "content": prompt_text}
    ],
    "temperature": 0,
    "top_p":0.2
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code != 200:
    print("Groq API error:", response.status_code)
    print(response.text)
    exit()

# --- Step 3: Clean the SQL --- #
raw_output = response.json()["choices"][0]["message"]["content"].strip()

# Remove markdown backticks if any
if raw_output.startswith("```"):
    sql_query = raw_output.strip("```sql").strip("```").strip()
else:
    sql_query = raw_output

print("\n SQL Query Generated:\n")
print(sql_query)

# --- Step 4: Save SQL to output file --- #
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
sql_path = os.path.join(OUTPUT_DIR, f"sql_response_{timestamp}.sql")
with open(sql_path, "w") as f:
    f.write(sql_query)

# --- Step 5: Run SQL in BigQuery --- #
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
bq_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

print("\n⏳ Running SQL query in BigQuery...")

try:
    query_job = bq_client.query(sql_query)
    result_df = query_job.to_dataframe()
    print("\n BigQuery Results:\n")
    print(result_df)
except Exception as e:
    print(" Error running query in BigQuery:")
    print(e)
