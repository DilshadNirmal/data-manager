from pymongo import MongoClient

try: 
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)

    database = client["sensor-data"]
    collection = database["sensors"]

    # results = collection.count_documents({})
    results = collection.find({})

    # print(results)

    buffer = []
    for doc in results:
        if doc['network']:
            for buffered_doc in buffer:
                print(f"{buffered_doc['network']} \n")
            buffer = []
            print(f"{doc}\n")
        else:
            buffer.append(doc)

    for doc in buffer:
        print(f"{doc}\n")

    client.close()

except Exception as e:
    raise Exception("the following error occured: ", e)