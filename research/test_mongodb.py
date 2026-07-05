import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)

try:
    # Ping the server
    client.admin.command("ping")
    print(" Connected to MongoDB Atlas successfully!")

    # List databases
    print("Databases:", client.list_database_names())

except Exception as e:
    print("Connection failed")
    print(e)