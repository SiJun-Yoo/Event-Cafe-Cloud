import pymongo

class DB(object):

    URI = "mongodb://localhost:27017"

    @staticmethod
    def init():
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['event_cafe_cloud']

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert_one(data)


    @staticmethod
    def find_one(collection, query):
        return DB.DATABASE[collection].find_one(query)


