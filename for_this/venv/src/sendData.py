from pymongo import MongoClient
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def fetch_new_records(collection, last_timestamp):
    query = {"createdAt": {"$gt": last_timestamp}} if last_timestamp else {}
    return list(collection.find(query).sort("createdAt", 1))

def process_true_record(collection, true_record, last_timestamp):
    # Query for false records with the updated schema
    false_query = {
        "network": False,
        "createdAt": {"$gte": last_timestamp, "$lte": true_record["createdAt"]}
    }
    logging.info(f"False query: {false_query}")
    return list(collection.find(false_query).sort("createdAt", 1))

def save_to_uploaded_again(collection, doc):
    try:
        # Save the document to the `uploaded-again` collection
        collection.update_one(
            {"_id": doc["_id"]},  # Match by `_id`
            {"$setOnInsert": doc},  # Insert the document if it doesn't exist
            upsert=True  # Perform upsert operation
        )
        logging.info(f"Document saved: {doc['_id']}")
    except Exception as e:
        logging.error(f"Error saving document: {e}")

def get_data():
    try:
        CONN_STRING = "mongodb://localhost:27017/"
        with MongoClient(CONN_STRING) as client:
            database = client["sensor-data"]
            sensors_collection = database["sensors"]
            uploaded_again_collection = database["uploaded-again"]

            last_processed_timestamp = None
            idx = 0

            while True:
                # Fetch new records
                new_docs = fetch_new_records(sensors_collection, last_processed_timestamp)
                if new_docs:
                    for doc in new_docs:
                        idx += 1
                        logging.info(f"Processing document: {doc}")
                        if doc["network"]:
                            # Process related false records and save them
                            false_docs = process_true_record(sensors_collection, doc, last_processed_timestamp)
                            for false_doc in false_docs:
                                save_to_uploaded_again(uploaded_again_collection, false_doc)

                            # Save the true record
                            save_to_uploaded_again(uploaded_again_collection, doc)
                        else:
                            # Update last processed timestamp for false records
                            if last_processed_timestamp is None:
                                last_processed_timestamp = doc["createdAt"]
                                logging.info(f"Updated last_processed_timestamp: {last_processed_timestamp}")
                else:
                    logging.info("No new records found. Waiting...")
                time.sleep(120)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    get_data()
