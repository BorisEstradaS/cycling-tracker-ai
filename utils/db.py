import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client[os.getenv("MONGO_DB", "cycling_db")]

def get_all_rides():
    db = get_db()
    return list(db.rides.find({}, {"trackpoints": 0}))  # Sin trackpoints para listar

def get_ride_by_id(ride_id):
    from bson import ObjectId
    db = get_db()
    return db.rides.find_one({"_id": ObjectId(ride_id)})

def insert_ride(ride_data):
    db = get_db()
    result = db.rides.insert_one(ride_data)
    return str(result.inserted_id)