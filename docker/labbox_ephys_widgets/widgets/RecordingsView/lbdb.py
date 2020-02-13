import os
from typing import Union, Tuple, Optional, List, Dict
import pymongo

class _MongoClient:
    def __init__(self):
        self._url = None
        self._client = None
    def insert_one(self, *, collection, doc, config):
        db = self._get_db(collection=collection, config=config)
        if not db:
            return None
        db.insert_one(doc)
    def find(self, *, collection, query, config):
        db = self._get_db(collection=collection, config=config)
        if not db:
            raise Exception('No db.')
        ret = []
        for doc in db.find(query):
            if '_id' in doc: del doc['_id']
            ret.append(doc)
        return ret
    def update(self, *, collection, query, update, config, upsert=False):
        db = self._get_db(collection=collection, config=config)
        if not db:
            raise Exception('No db.')
        db.update(query, update, upsert=upsert)
    def remove(self, *, collection, query, config):
        db = self._get_db(collection=collection, config=config)
        if not db:
            raise Exception('No db.')
        db.remove(query)
    def _get_db(self, *, collection, config):
        url = config['url']
        database = config['database']
        if config.get('password', None) is not None:
            url = url.replace('${password}', config['password'])
        if url != self._url:
            if self._client is not None:
                self._client.close()
            self._client = pymongo.MongoClient(url, retryWrites=False)
            self._url = url
        return self._client[database][collection]

_global_client = _MongoClient()

_mongo_host = os.getenv('MONGO_HOST', 'localhost')
_global_config = dict(
    url=f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASSWORD']}@{_mongo_host}:{os.environ['MONGO_PORT']}",
    database='labbox'
)

def insert_one(*, collection: str, doc: dict):
    return _global_client.insert_one(collection=collection, doc=doc, config=_global_config)

def update(*, collection, query, update, upsert=False):
    _global_client.update(collection=collection, query=query, update=update, config=_global_config, upsert=upsert)

def find(*, collection, query):
    return _global_client.find(collection=collection, query=query, config=_global_config)

def remove(*, collection, query):
    return _global_client.remove(collection=collection, query=query, config=_global_config)
