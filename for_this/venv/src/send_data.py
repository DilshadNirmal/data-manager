from pymongo import MongoClient
import time

def get_data():
    try:
        # MongoDB connection
        CONN_STRING = "mongodb://localhost:27017/"
        client = MongoClient(CONN_STRING)
        database = client["sensor-data"]
        collection = database["sensors"]

        # Variable to track the last processed timestamp
        last_processed_timestamp = None
        idx = 0

        while True:
            # Query for new documents
            query = {}
            if last_processed_timestamp:
                query = {"createdAt": {"$gt": last_processed_timestamp}}

            # Fetch new records sorted by createdAt
            new_docs = list(collection.find(query).sort("createdAt", 1))

            if new_docs:
                for doc in new_docs:
                    idx += 1
                    created_at = doc["createdAt"]

                    if doc["network"]:  # If the record has network = true
                        print(f"{idx} => \n Processing true record: {doc}")

                        # Fetch and process all false records with createdAt <= current true record's createdAt
                        false_query = {"network": False, "createdAt": {"$gt": last_processed_timestamp, "$lte": created_at}}
                        false_docs = list(collection.find(false_query).sort("createdAt", 1))

                        for false_doc in false_docs:
                            idx += 1
                            print(f"{idx} => \n Processing false record: {false_doc}")

                    # Update last_processed_timestamp to the current record's createdAt
                    last_processed_timestamp = created_at

            else:
                print("No new records found. Waiting...")
            
            # Sleep to avoid continuous polling
            time.sleep(120)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    get_data()
