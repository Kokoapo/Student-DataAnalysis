import pandas as pd
import kagglehub
import os

DOWNLOAD_PATH = "./datasets"

class Database: 
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.path = None
        self.dataset = None

    def download(self):
        self.path = kagglehub.dataset_download(self.dataset_name, output_dir=DOWNLOAD_PATH)
        print(f"Dataset downloaded to: {self.path}")

    def read(self):
        if self.path is None:
            raise ValueError("Dataset not downloaded yet. Please call the download method first.")

        name = None
        for file in os.listdir(self.path):
            if file.endswith(".csv"):
                name = file

        self.dataset = pd.read_csv(os.path.join(self.path, name))
        print(self.dataset.head())

    def get_dataset(self):
        if self.dataset is None:
            raise ValueError("Dataset not read yet. Please call the read method first.")
        return self.dataset
    
