#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
from pymongo import MongoClient, GEO2D
from pymongo.errors import BulkWriteError
from boi.config import MongoConfig


_client = MongoClient(MongoConfig.HOST, MongoConfig.PORT)
_db = _client[MongoConfig.DATABASE]


def init_collection(session):
    _collection = _db[session]
    _collection.remove({})
    _collection.create_index([('loc', GEO2D)])


def write_idxs(arr, session):
    _collection = _db['idxs']
    _collection.delete_one(dict(session=session, ))
    _collection.insert_one(dict(
        session=session,
        idxs=[int(x) for x in arr]
    ))


def get_idx(idx, session):
    _collection = _db['idxs']
    _docs = _collection.find_one(dict(session=session, ))['idxs'][idx]
    return _docs


def get_shuffled_idxs(ordered_idxs, session_id):
    _collection = _db['idxs']
    _docs = _collection.find_one(dict(
        session=session_id,
    ))['idxs'][ordered_idxs[0]:ordered_idxs[-1]+1]
    return _docs


def write_pixel(x, y, c, session):
    _collection = _db[session]
    _collection.insert_one(dict(
        loc=[x, y], c=c
    ))


def write_pixels(pxls, session):
    _collection = _db[session]
    _requests = [dict(loc=[p['lon'], p['lat']], c=p['color']) for p in pxls]
    try:
        _collection.insert_many(_requests, ordered=False)
    except BulkWriteError as bwe:
        print(bwe.details)


def get_near(lonlat, _n, session):
    _collection = _db[session]
    # _docs = _collection.find({'loc': {'$near': lonlat}}, {'_id': 0}).limit(5)
    _docs = _collection.aggregate([
        {'$geoNear': {'near': lonlat, 'distanceField': 'dist'}},
        {'$limit': _n},
        {'$project': {'_id': 0}}
    ])
    return _docs


if __name__ == '__main__':
    pass
