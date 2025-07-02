# from google.cloud import bigquery

# # Define project, dataset, and table as variables
# project_id = "useful-maxim-462822-g4"
# dataset_id = "retail"

# # Initialize BigQuery client
# client = bigquery.Client(project=project_id)

# # Query to get all the tables in the dataset
# query_tables = f"""
#     SELECT table_name
#     FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.TABLES`
# """

# # Run the query and convert to DataFrame
# df_tables = client.query(query_tables).to_dataframe()

# # Show the result
# print("Tables in the dataset are: ", df_tables)

# # Query to get schema information
# query_schema = f"""
#     SELECT 
#       table_name,
#       column_name,
#       data_type
#     FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
#     ORDER BY table_name, ordinal_position
# """

# # Run query
# df_schema = client.query(query_schema).to_dataframe()

# # Convert to nested dictionary
# schema_dict = {}
# for row in df_schema.itertuples(index=False):
#     table = row.table_name
#     column_info = {"column_name": row.column_name, "data_type": row.data_type}
#     schema_dict.setdefault(table, []).append(column_info)

# # Print the nested dictionary
# from pprint import pprint
# print("Schema dictionary:")
# pprint(schema_dict)

import argparse
import json
from pprint import pprint
from google.cloud import bigquery
from google.oauth2 import service_account

def get_bigquery_schema(credentials_path, project_id, dataset_id):
    # Authenticate using the service account
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(project=project_id, credentials=credentials)

    # Query for schema information
    query_schema = f"""
        SELECT 
            table_name,
            column_name,
            data_type
        FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
        ORDER BY table_name, ordinal_position
    """

    df_schema = client.query(query_schema).to_dataframe()

    # Construct schema dictionary
    schema_dict = {}
    for row in df_schema.itertuples(index=False):
        schema_dict.setdefault(row.table_name, []).append({
            "column_name": row.column_name,
            "data_type": row.data_type
        })

    return json.dumps(schema_dict, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Fetch BigQuery table schemas.")
    parser.add_argument("--credentials", required=True, help="Path to GCP service account JSON file")
    parser.add_argument("--project_id", required=True, help="GCP project ID")
    parser.add_argument("--dataset_id", required=True, help="BigQuery dataset ID")

    args = parser.parse_args()

    schema_json = get_bigquery_schema(args.credentials, args.project_id, args.dataset_id)
    print("BigQuery Schema Dictionary:")
    print(schema_json)


if __name__ == "__main__":
    main()


# python get_bq_schema.py \
#   --credentials credentials.json \
#   --project_id useful-maxim-462822-g4 \
#   --dataset_id retail
