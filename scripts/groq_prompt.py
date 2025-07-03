import requests
import json
import os
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration --- #
GROQ_API_KEY = "YOUR_GROQ_API"  
MODEL = "llama3-8b-8192"
PROMPT_FILE = "llama_prompt.txt"
OUTPUT_DIR = "../outputs"
PROJECT_ID = "your-gcp-project-id" 
CREDENTIALS_FILE = "path/to/your/credentials.json"

# === SETUP === #
os.makedirs(OUTPUT_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# === STEP 1: Read prompt === #
with open(PROMPT_FILE, "r") as f:
    full_prompt = f.read().strip()

# Extract only the last line (the user’s natural question)
lines = full_prompt.splitlines()
user_question = ""
for line in reversed(lines):
    if line.strip():  # get the last non-empty line
        user_question = line.strip()
        break

# === STEP 2: Get SQL from Groq === #
print("Generating SQL from LLaMA...")

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

sql_generation_payload = {
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
        {"role": "user", "content": user_question}
    ],
    "temperature": 0,
    "top_p": 0.2
}

response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(sql_generation_payload))

if response.status_code != 200:
    print("Groq API Error:", response.status_code)
    print(response.text)
    exit()

sql_raw = response.json()["choices"][0]["message"]["content"].strip()
sql_query = sql_raw.strip("```sql").strip("```").strip() if sql_raw.startswith("```") else sql_raw

print("\nSQL Query Generated:\n")
print(sql_query)

# === STEP 3: Save SQL to file === #
sql_file = os.path.join(OUTPUT_DIR, f"sql_response_{timestamp}.sql")
with open(sql_file, "w") as f:
    f.write(sql_query)

# === STEP 4: Run SQL in BigQuery === #
print("\nRunning query in BigQuery...")

credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
bq_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

try:
    query_job = bq_client.query(sql_query)
    result_df = query_job.to_dataframe()
    print("\nQuery Results:\n")
    print(result_df)

    # === STEP 5: Save question, SQL, and results to .json === #
    result_json = {
        "question": user_question,
        "sql_query": sql_query,
        "results": result_df.to_dict(orient="records")
    }

    json_file = os.path.join(OUTPUT_DIR, f"response_{timestamp}.json")
    with open(json_file, "w") as f:
        json.dump(result_json, f, indent=2)

    print(f"\nJSON response saved to: {json_file}")

    # === STEP 6: Ask Groq for Business Insight (no schema) === #
    insight_prompt = (
        f"The following is a user question about a business dataset:\n"
        f"{user_question}\n\n"
        f"Provide only a concise business insight in plain English. "
        f"Do not include any SQL, schema, or restate the question. "
        f"Just return the insight itself."
    )

    insight_payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a business analyst generating insights from SQL query results. "
                    "Your goal is to summarize key takeaways for a non-technical audience."
                )
            },
            {"role": "user", "content": insight_prompt}
        ],
        "temperature": 0.3
    }

    print("\nRequesting business insight from LLaMA...")

    insight_response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(insight_payload))

    if insight_response.status_code == 200:
        insight_text = insight_response.json()["choices"][0]["message"]["content"].strip()
        print("\nBusiness Insight:\n")
        print(insight_text)

        # === STEP 7: Save insight and question to .txt === #
        insight_file = os.path.join(OUTPUT_DIR, f"insight_{timestamp}.txt")
        with open(insight_file, "w") as f:
            f.write(f"User Question:\n{user_question}\n\n")
            f.write("Business Insight:\n")
            f.write(insight_text.strip())

        print(f"\nInsight saved to: {insight_file}")
    else:
        print("Error generating insight:", insight_response.status_code)
        print(insight_response.text)

except Exception as e:
    print("Error running SQL in BigQuery:")
    print(e)