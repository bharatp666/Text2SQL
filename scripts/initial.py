from google.cloud import bigquery

# Define project, dataset, and table as variables
project_id = "useful-maxim-462822-g4"
dataset_id = "retail"

# Initialize BigQuery client
client = bigquery.Client(project=project_id)

# Query to get all the tables in the dataset
query = f"""
    SELECT table_name
    FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.TABLES`
"""

# Run the query and convert to DataFrame
df = client.query(query).to_dataframe()

# Show the result
print("Tables in the dataset are: ", df)