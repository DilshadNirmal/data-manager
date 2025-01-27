from pymongo import MongoClient
import time

def get_data():
    try:
        # MongoDB connection
        CONN_STRING = "mongodb://localhost:27017/"
        client = MongoClient(CONN_STRING)
        database = client["sensor-data"]
        collection = database["sensors"]

        # Variable to track the last processed false record's createdAt timestamp
        last_processed_timestamp = None
        idx = 0

        while True:
            # Query for new documents
            query = {}
            if last_processed_timestamp:
                query = {"createdAt": {"$gt": last_processed_timestamp}}

            # Fetch new records sorted by createdAt
            new_docs = list(collection.find(query).sort("createdAt", 1))

            for doc in new_docs:
                idx += 1
                if doc["network"]:  # If the record has network = true
                    print(f"{idx} => \n Processing true record: {doc}")

                    # Fetch and process all false records with createdAt > last_processed_timestamp
                    if last_processed_timestamp:
                        false_query = {"network": False, "createdAt": {"$gt": last_processed_timestamp}}
                        false_docs = list(collection.find(false_query).sort("createdAt", 1))

                        if false_docs:
                            print(f"Processing false records from {last_processed_timestamp}:")
                            for false_doc in false_docs:
                                print(f"{idx} => \n {false_doc}")

                            # Update last processed timestamp to the last false record's createdAt
                            last_processed_timestamp = false_docs[-1]["createdAt"]

                else:  # If the record has network = false
                    # Update the last processed timestamp for false records
                    last_processed_timestamp = doc["createdAt"]

            # Sleep to avoid continuous polling
            time.sleep(90)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    get_data()
