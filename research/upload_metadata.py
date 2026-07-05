import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))

db = client[os.getenv("DATABASE_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

# Dataset path
dataset_path = "research/CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone"

# Remove old data
collection.delete_many({})

count = 0

for label in os.listdir(dataset_path):

    label_path = os.path.join(dataset_path, label)

    if not os.path.isdir(label_path):
        continue

    for image_name in os.listdir(label_path):

        if image_name.lower().endswith((".jpg", ".jpeg", ".png")):

            document = {
                "image_name": image_name,
                "label": label,
                "image_path": os.path.join(label_path, image_name)
            }

            collection.insert_one(document)
            count += 1

print(f"Successfully uploaded {count} image metadata.")