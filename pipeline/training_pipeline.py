from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.model_training import ModelTraining

if __name__=="__main__":

    # data_ingestion = DataIngestion()
    # data_ingestion.download_csv_from_minio()

    data_processor = DataProcessing("artifacts/raw/data.csv")
    data_processor.run()

    model_trainer = ModelTraining()
    model_trainer.run()