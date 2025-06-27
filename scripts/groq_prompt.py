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
GROQ_API_KEY = "<YOUR_GROQ_API_KEY>"
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

data = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant that generates BigQuery compliant SQL queries. Explicitly mention the dataset_id along with table names in your queries."},
        {"role": "user", "content": prompt_text}
    ],
    "temperature": 0
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