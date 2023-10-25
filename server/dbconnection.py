import pymongo
from datetime import datetime
from bson.objectid import ObjectId
import logging

class DB_connection:
    def __init__(self, credentials):
        self.mongo_client = pymongo.MongoClient(credentials["address"])
        self.database = self.get_database(credentials["name"])
        self.limit = credentials["limit"]

    def get_database(self, db_name):
        db_list = self.mongo_client.list_database_names()
        if db_name not in db_list:
            logging.warning(f"Database '{db_name}' was created.")
        mydb=self.mongo_client[db_name]
        return mydb

    def get_collection(self, collection_name):
        collection_list = self.database.list_collection_names()
        logging.debug(collection_list)
        if collection_name not in collection_list:
            logging.warning(f"Collection {collection_name} was added.")
        return self.database[collection_name]

#   1-st variable type dict, 2-nd collection name to save
    def add_one_record(self, record, collection_name):
        db_collection = self.get_collection(collection_name)
        record_id = db_collection.insert_one(record)
        return record_id.inserted_id
#   Search by date(ISODate) and _id
    def get_records(self, field, collection_name):
        db_collection = self.get_collection(collection_name)
        if field['key'] == 'record_id':
            document = db_collection.find({"_id": ObjectId(field["value"])}).limit(self.limit)
            return document
        if field['key'] == 'date':
            dt=datetime.fromisoformat(field["value"])
            document = db_collection.find({"date": {"$gte": dt}}).limit(self.limit)
        else:
            logging.info("Wrong key")
            document = None
        return document
        
    def delete_one(self, record_id, collection_name):
        db_collection = self.get_collection(collection_name)
        message = db_collection.delete_one({"_id": ObjectId(record_id)})
        logging.debug(message)
#   To update pass record_id(_id in database), collection name and new record
    def update_one(self, record_id, new_record, collection_name):
        db_collection = self.get_collection(collection_name)
        message = db_collection.update_one({"_id": ObjectId(record_id)}, {"$set": new_record})
        logging.debug(message)

