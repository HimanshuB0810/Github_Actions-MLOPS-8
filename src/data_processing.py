import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
import os

from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class DataProcessing:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.processed_data_path = "artifacts/processed"
        os.makedirs(self.processed_data_path,exist_ok=True)

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            logger.info("Read the Data Successfully")

        except Exception as e:
            logger.error(f"Error while reading the data {e}")
            raise CustomException("Failed to read the data",e)
        
    def handle_outliers(self,column):
        try:
            logger.info("Starting Handling Outliers")
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)

            IQR = Q3-Q1

            Lower_value = Q1-1.5*IQR
            Upper_value = Q3+1.5*IQR

            sepal_median = np.median(self.df[column])

            for i in self.df[column]:
                if i>Upper_value or i<Lower_value:
                    self.df[column] = self.df[column].replace(i,sepal_median)

            logger.info("Handled Outliers Successfully")

        except Exception as e:
            logger.error(f"Error while Handling Outliers {e}")
            raise CustomException("Failed to Handle Outliers",e)
        
    def split_data_and_Saving(self):
        try:
            X = self.df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
            Y = self.df['Species']

            X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

            logger.info("Data Splitted Successfully")

            joblib.dump(X_train,os.path.join(self.processed_data_path,"X_train.pkl"))
            joblib.dump(X_test,os.path.join(self.processed_data_path,"X_test.pkl"))
            joblib.dump(y_train,os.path.join(self.processed_data_path,"y_train.pkl"))
            joblib.dump(y_test,os.path.join(self.processed_data_path,"y_test.pkl"))

            logger.info("Files Saved Successfully for Data Processing Step")
        
        except Exception as e:
            logger.error(f"Error while spiltting data {e}")
            raise CustomException("Failed to splitting data",e)
        
    def run(self):
        try:
            self.load_data()
            self.handle_outliers("SepalWidthCm")
            self.split_data_and_Saving()

            logger.info("Data Processing Step Completed")

        except Exception as e:
            logger.error(f"Error in the Data Processing Step {e}")
            raise CustomException("Failed in the Data Processing Step",e)
        
if __name__=="__main__":
    data_processor = DataProcessing("artifacts/raw/data.csv")
    data_processor.run()