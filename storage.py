import json
from azure.storage.blob import BlobServiceClient
import os
import logging


def upload_raw_to_blob(blob_service, filename, weather_data):
    blob = blob_service.get_blob_client(filename)

    with open(filename, "w") as file:
        json.dump(weather_data, file, indent=4)

    with open(filename, 'rb') as file:
        blob.upload_blob(file, overwrite=True)

    logging.info("Successfully uploaded raw JSON into Azure Blob Storage")



connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service = BlobServiceClient.from_connection_string(connection_string)
container = blob_service.get_container_client('weathercontainer')



