from pymongo import MongoClient

def get_data():
    try:
        CONN_STRING = "mongodb://localhost:27017/"
        client = MongoClient(CONN_STRING)
        database = client["sensor-data"]
        collection = database["sensors"]
        documents = collection.find({})
        length = collection.count_documents({})
        print(length)

        store_last_createdAt = 0
        idx = 0
        networkStaus = documents[0]['network']
        for doc in documents:
            idx += 1
            if networkStaus:
                networkStaus = doc['network']
                print(f"{idx} => {doc['createdAt']} : {doc['network']} : {doc['sensor']}")
            else:
                networkStaus = doc['network']
                if isinstance(store_last_createdAt, str):
                    store_last_createdAt = store_last_createdAt
                    print(f"{idx} => last false value: {store_last_createdAt} \t")
                else:
                    store_last_createdAt = str(doc['createdAt'])

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    get_data()