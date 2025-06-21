from google.cloud import bigquery

# Define project, dataset, and table as variables
project_id = "useful-maxim-462822-g4"
dataset_id = "retail"

# Initialize BigQuery client
client = bigquery.Client(project=project_id)

# Query to get all the tables in the dataset
query_tables = f"""
    SELECT table_name
    FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.TABLES`
"""

# Run the query and convert to DataFrame
df_tables = client.query(query_tables).to_dataframe()

# Show the result
print("Tables in the dataset are: ", df_tables)

# Query to get schema information
query_schema = f"""
    SELECT 
      table_name,
      column_name,
      data_type
    FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
    ORDER BY table_name, ordinal_position
"""

# Run query
df_schema = client.query(query_schema).to_dataframe()

# Convert to nested dictionary
schema_dict = {}
for row in df_schema.itertuples(index=False):
    table = row.table_name
    column_info = {"column_name": row.column_name, "data_type": row.data_type}
    schema_dict.setdefault(table, []).append(column_info)

# Print the nested dictionary
from pprint import pprint
print("Schema dictionary:")
pprint(schema_dict)
