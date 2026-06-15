import os
import pandas as pd
from src.custom_exception import CustomException
from src.logger import get_logger
from minio import Minio

RAW = "artifacts/raw"

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self):
        self.bucket_name = "iris-dataset"
        self.bucket_file_name = "data.csv"

        os.makedirs(RAW,exist_ok=True)

        logger.info(f"Data Ingestion Started")

    def download_csv_from_minio(self):
        try:
            client = Minio(
                "192.168.1.13:9000",
                access_key="minioadmin",
                secret_key="minioadmin",
                secure=False
            )

            local_file = os.path.join(RAW,"data.csv")

            client.fget_object(
                self.bucket_name,
                self.bucket_file_name,
                local_file
            )
            logger.info("Raw file successfully downloaded from Minio to {RAW}")
        except Exception as e:
                logger.error("Error while downloading CSV file from MinIO")
                raise CustomException("Failed to download csv file from MinIO", e)
        

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion.download_csv_from_minio()