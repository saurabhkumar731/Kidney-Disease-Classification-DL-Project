import os
import shutil
from pymongo import MongoClient
from dotenv import load_dotenv

from cnnClassifier import logger
from cnnClassifier.entity.config_entity import DataIngestionConfig

load_dotenv()


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def fetch_data_from_mongodb(self):

        logger.info("Connecting to MongoDB...")

        client = MongoClient(os.getenv("MONGODB_URI"))

        db = client[self.config.database_name]
        collection = db[self.config.collection_name]

        documents = collection.find()

        os.makedirs(self.config.root_dir, exist_ok=True)

        count = 0

        for doc in documents:

            image_path = os.path.normpath(doc["image_path"])
            label = doc["label"]

            destination_folder = os.path.join(self.config.root_dir, label)
            os.makedirs(destination_folder, exist_ok=True)

            destination_path = os.path.join(
                destination_folder,
                os.path.basename(image_path)
            )

            if os.path.exists(image_path):
                shutil.copy2(image_path, destination_path)
                count += 1
            else:
                logger.warning(f"Image not found: {image_path}")

        logger.info(f"Successfully copied {count} images.")