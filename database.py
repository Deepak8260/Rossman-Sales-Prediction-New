from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client['rossman_predictions']
        self.predictions = self.db['predictions']

    def save_prediction(self, features, prediction):
        prediction_data = {
            'timestamp': datetime.now(),
            'features': features,
            'predicted_sales': float(prediction)
        }
        return self.predictions.insert_one(prediction_data)

    def get_all_predictions(self):
        return list(self.predictions.find({}, {'_id': 0}))

    def get_predictions_by_store(self, store_id):
        return list(self.predictions.find({'features.store': store_id}, {'_id': 0}))

    def get_recent_predictions(self, limit=10):
        return list(self.predictions.find({}, {'_id': 0}).sort('timestamp', -1).limit(limit))