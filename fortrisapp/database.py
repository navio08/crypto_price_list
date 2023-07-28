import pymongo
from config import HOST_MONGO

connection = f"mongodb://root:pass@{HOST_MONGO}:27017"
mongo = pymongo.MongoClient(connection)["Fortris"]["prices"]
