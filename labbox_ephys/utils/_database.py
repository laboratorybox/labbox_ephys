import os
import hither2 as hi

def database():
    return hi.Database(mongo_url=os.environ['MONGO_URI'], database='labbox')

def dbcollection(collection):
    db = database()
    return db.collection(collection)