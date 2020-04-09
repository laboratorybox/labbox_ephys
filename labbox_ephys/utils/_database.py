import os
import hither2 as hi

def database():
    return hi.Database(mongo_url=os.environ['LABBOX_EPHYS_MONGO_URI'], database='labbox')

def dbcollection(collection):
    db = database()
    return db.collection(collection)

def remote_job_handler():
    return hi.RemoteJobHandler(
        database=database(),
        compute_resource_id=os.environ['LABBOX_EPHYS_COMPUTE_RESOURCE_ID']
    )

def job_cache():
    return hi.JobCache(
        database=database()
    )