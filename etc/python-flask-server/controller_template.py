import connexion
import six

from flask import abort
from swagger_server import util

from kombu import Connection, Producer, Exchange, Queue
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from bson import json_util
from bson.objectid import ObjectId
import os
import time
import sys
import json
import uuid
import bsonjs
from bson.raw_bson import RawBSONDocument
import redis

KEY = "${KEY}"
CUSTOM_KEY = "${CUSTOM_KEY}"
SOFT_DELETE = os.getenv('SOFT_DELETE_FLAG', False)

def dpath(dict_data):
    if not CUSTOM_KEY:
        return ''
    try:
        paths = CUSTOM_KEY.split(".")
        data = dict_data
        for i in range(0,len(paths)):
            data = data[paths[i]]
        return '.{}'.format(data)
    except:
        return ''

try:
    ## mongodb connection
    client = MongoClient('mongodb://{}:{}/'.format(os.getenv('MONGODB_HOST'),os.getenv('MONGODB_PORT')), document_class=RawBSONDocument)
    db = client[os.getenv('MONGODB_DB', 'v2')]
    collection = db[KEY]
    ## rabbitmq connection
    connection = Connection('amqp://{}:{}@{}:{}//'.format(os.getenv('RABBITMQ_DEFAULT_USER'),os.getenv('RABBITMQ_DEFAULT_PASS'),os.getenv('RABBITMQ_HOST'),os.getenv('RABBITMQ_PORT')))
    exchange = Exchange(KEY, type='topic')
    producer = Producer(connection, exchange=exchange)
    publisher = connection.ensure(producer, producer.publish, max_retries=5)
    ## redis connection
    r = redis.StrictRedis(host=os.getenv("REDIS_HOST"), db=int(os.getenv("REDIS_DB")))
except:
    time.sleep(1)
    sys.exit(1)


def create${KEY}(body=None):  # noqa: E501
    """Create a new ${KEY}

     # noqa: E501

    :param body: ${KEY} to be created
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = connexion.request.get_json()  # noqa: E501

    doc_id = str(uuid.uuid4())
    body['_id'] = doc_id
    body['_sys'] = {'created_ts': int(time.time()), 'created_by': connexion.request.headers['x-api-user']}
    body_str = json.dumps(body)
    collection.insert_one(RawBSONDocument(bsonjs.loads(body_str)))

    routingKey='{}{}.{}'.format(KEY, dpath(body), 'create')
    queues = [Queue(routingKey, exchange=exchange, routing_key=routingKey)]
    publisher(body_str, routing_key=routingKey, retry=True, declare=queues, headers={'_id':doc_id})

    skey = '{}|{}'.format(KEY, doc_id)
    r.set(skey, body_str)
    r.delete(KEY)

    return doc_id


def delete${KEY}(ID):  # noqa: E501
    """Delete the ${KEY} instance based on ID

     # noqa: E501

    :param ID: 
    :type ID: str

    :rtype: None
    """
    skey = '{}|{}'.format(KEY, ID)
    r.delete(skey)
    r.delete(KEY)
    q = {'_id': ID}
    doc_mongo = collection.find_one_and_delete(q)
    doc_str = bsonjs.dumps(doc_mongo.raw)

    routingKey='{}{}.{}'.format(KEY, dpath(json.loads(doc_str)), 'delete')
    queues = [Queue(routingKey, exchange=exchange, routing_key=routingKey)]
    publisher(doc_str, routing_key=routingKey, retry=True, declare=queues, headers=q)



def get_all${KEY}(offset=0, limit=20, q=None, p=None, sort=None, order=1):  # noqa: E501
    """Get the list of all ${KEY}

     # noqa: E501

    :param offset: The number of items to skip before starting to collect the result set.
    :type offset: int
    :param limit: The numbers of items to return.
    :type limit: int
    :param q: The stringify json query
    :type q: str
    :param sort: The sorting field
    :type sort: str
    :param order: The sorting order where 1 is asc and -1 is desc.
    :type order: int

    :rtype: List[${KEY}]
    """
    hkey = '{}|{}|{}|{}|{}|{}'.format(q, p, offset, limit, sort, order)
    cache = r.hget(KEY, hkey)
    if cache:
        return json.loads(cache)

    try:
        filter_json = json.loads(q) if q is not None else None
        projec_json = json.loads(p) if p is not None else None
        sort_json = [(sort, order)] if sort is not None else None
    except:
        abort(400)

    docs = collection.find(filter=filter_json, projection=projec_json, skip=offset, limit=limit, sort=sort_json)
    count = collection.count_documents(filter_json or {})
    response = { 'total': count, 'results': [json.loads(bsonjs.dumps(doc.raw)) for doc in docs] }
    r.hset(KEY, hkey, json.dumps(response))
    return response


def get${KEY}(ID):  # noqa: E501
    """Get the ${KEY} instance based on ID

     # noqa: E501

    :param ID: 
    :type ID: str

    :rtype: ${KEY}
    """
    skey = '{}|{}'.format(KEY, ID)
    doc_str = r.get(skey)
    if not doc_str:
        doc = collection.find_one({'_id': ID})
        doc_str = bsonjs.dumps(doc.raw)
        r.set(skey, doc_str)
    return json.loads(doc_str)


def update${KEY}(ID, body=None):  # noqa: E501
    """Update the ${KEY} instance based on ID

     # noqa: E501

    :param ID: 
    :type ID: str
    :param body: Updated ${KEY} instance
    :type body: dict | bytes

    :rtype: None
    """
    skey = '{}|{}'.format(KEY, ID)
    r.delete(skey)
    r.delete(KEY)

    if connexion.request.is_json:
        body = connexion.request.get_json()  # noqa: E501
    body['_sys']['updated_ts'] = int(time.time())
    body['_sys']['updated_by'] = connexion.request.headers['x-api-user']
    collection.replace_one({'_id': ID}, body)

    routingKey='{}{}.{}'.format(KEY, dpath(body), 'update')
    queues = [Queue(routingKey, exchange=exchange, routing_key=routingKey)]
    publisher(json.dumps(body), routing_key=routingKey, retry=True, declare=queues, headers={'_id':ID})
