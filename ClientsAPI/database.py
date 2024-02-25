import pymongo
from variables import *
# Connect to MongoDB
mongo_url = "mongodb+srv://SUBHAM:MONGODB123@subham.h15frqq.mongodb.net/?retryWrites=true&w=majority"

def updateDatabase(query, update):
    client = pymongo.MongoClient(mongo_url)
    db = client.subham  
    collection = db.pc_details      
    
    update_result = collection.update_one(query, update, upsert=True)

    if update_result.acknowledged:
        if update_result.upserted_id:
            print("Inserted document with ID:", update_result.upserted_id)
        else:
            if update_result.modified_count > 0:
                print("Updated document:", update_result.modified_count)
            else:
                print("No documents matched the query.")
    else:
        print("Write operation not acknowledged. Update failed.")
    
    client.close()

def all_details():
    client = pymongo.MongoClient(mongo_url)
    db = client.subham  
    collection = db.pc_details
    details =  list(collection.find())
    client.close()
    return details

def makeLength10():
    details = all_details()
    
    for data in details:
        try:
        
            if len(data['usage_data']) > 10:
                finalData = data['usage_data'][len(data['usage_data'])-11:len(data['usage_data'])-1]
                
                updateDatabase({"pc_name": pc_name}, {"$set":{"usage_data": finalData}})
                
        except: 
            continue
