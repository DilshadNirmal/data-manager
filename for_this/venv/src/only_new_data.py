from pymongo import MongoClient
import time

def monitor_and_save():
    try:
        uri = "mongodb://localhost:27017/"
        client = MongoClient(uri)
        database = client["sensor-data"]
        collection = database["sensors"]

        buffer = []

        last_processed_id = None

        while True:
            query = {} if last_processed_id is None else { "_id": {"$gt": last_processed_id}}
            new_docs = list(collection.find(query).sort("_id", 1))

            for doc in new_docs:
                last_processed_id = doc["_id"]

                if doc["network"]:
                    if buffer:
                        for buffered_doc in buffer:
                            print(buffered_doc)
                        
                        buffer = []
                    
                    print(f"Processing document with network: true\n{doc}\n")
                else: 
                    buffer.append(doc)
            
            time.sleep(5)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    monitor_and_save()