from pymongo import MongoClient
from datetime import datetime
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def fetch_new_records(collection, last_timestamp):
    """Fetch new records from the collection since the last processed timestamp."""
    query = {"createdAt": {"$gt": last_timestamp}} if last_timestamp else {}
    return list(collection.find(query).sort("createdAt", 1))

def process_true_record(collection, true_record, first_false_timestamp):
    """Fetch and process False records between first_false_timestamp and the True record's timestamp."""
    false_query = {
        "network": False,
        "createdAt": {"$gte": first_false_timestamp, "$lte": true_record["createdAt"]}
    }
    logging.info(f"False query: {false_query}")
    return list(collection.find(false_query).sort("createdAt", 1))

def get_data():
    try:
        CONN_STRING = "mongodb://localhost:27017/"
        with MongoClient(CONN_STRING) as client:
            database = client["sensor-data"]
            collection = database["sensors"]

            last_processed_timestamp = None
            first_false_timestamp = None  # Track the first False timestamp
            buffered_true_record = None  # Buffer the first True record after False
            idx = 0

            while True:
                new_docs = fetch_new_records(collection, last_processed_timestamp)
                if new_docs:
                    for doc in new_docs:
                        idx += 1
                        last_processed_timestamp = doc["createdAt"]  # Update last processed timestamp

                        if doc["network"]:
                            # If network is True, check if there are pending False records
                            if first_false_timestamp is not None:
                                # Process all False records first
                                false_docs = process_true_record(collection, doc, first_false_timestamp)
                                # logging.info(f"False records to process: {false_docs}")
                                for false_doc in false_docs:
                                    idx += 1
                                    logging.info(f"Processing false record: {false_doc}")

                                # Reset the first False timestamp after processing
                                first_false_timestamp = None

                                # Process the buffered True record
                                if buffered_true_record:
                                    logging.info(f"Processing buffered true record: {buffered_true_record}")
                                    buffered_true_record = None

                            # Buffer the current True record if there are no pending False records
                            if first_false_timestamp is None:
                                logging.info(f"Processing true record: {doc}")
                            else:
                                # Buffer the True record if there are pending False records
                                buffered_true_record = doc
                        else:
                            # If network is False, track the first False timestamp
                            if first_false_timestamp is None:
                                first_false_timestamp = doc["createdAt"]
                                logging.info(f"First False timestamp set to: {first_false_timestamp}")
                else:
                    logging.info("No new records found. Waiting...")
                time.sleep(6)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    get_data()