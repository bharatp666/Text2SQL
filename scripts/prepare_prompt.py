from google.cloud import bigquery
import json
from pprint import pprint

# --- CONFIG --- #
project_id = "useful-maxim-462822-g4"
dataset_id = "retail"
user_question = "List all customers who placed an order in 1998."
schema_file_path = "retail_schema.json"
prompt_output_path = "llama_prompt.txt"

# --- Step 1: Connect to BigQuery and Fetch Schema --- #
client = bigquery.Client(project=project_id)

query = f"""
    SELECT 
      table_name,
      column_name,
      data_type
    FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
    ORDER BY table_name, ordinal_position
"""

df = client.query(query).to_dataframe()

# --- Step 2: Convert to Nested Schema Dictionary --- #
schema_dict = {}
for row in df.itertuples(index=False):
    table = row.table_name
    column_info = {"column_name": row.column_name, "data_type": row.data_type}
    schema_dict.setdefault
    schema_dict.setdefault(table, []).append(column_info)

# schema_dict = {}
# for row in df.itertuples(index=False):
#     full_table_name = f"{row.dataset_id}.{row.table_name}"  # Add dataset_id prefix
#     column_info = {"column_name": row.column_name, "data_type": row.data_type}
#     schema_dict.setdefault(full_table_name, []).append(column_info)

# Optional: save schema_dict as JSON
with open(schema_file_path, "w") as f:
    json.dump(schema_dict, f, indent=2)

# --- Step 3: Format Schema as Natural Language --- #
def format_schema_for_prompt(schema):
    lines = ["Dataset:" + dataset_id]
    for table, columns in schema.items():
        lines.append(f"\nTable: {table}")
        for col in columns:
            lines.append(f"- {col['column_name']} ({col['data_type']})")
    return "\n".join(lines)

schema_text = format_schema_for_prompt(schema_dict)

# --- Step 4: Build Final Prompt --- #
prompt = f"""You are a helpful assistant that writes BigQuery SQL queries.

Here is the database schema:
{schema_text}

Now write a SQL query for this question:
{user_question}
"""

# --- Step 5: Output the Prompt --- #
print("\n--- Final Prompt for LLaMA ---\n")
print(prompt)

# Save to file
with open(prompt_output_path, "w") as f:
    f.write(prompt)