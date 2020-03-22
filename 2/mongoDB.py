from pymongo import MongoClient
import sys
sys.path.append('./')
import util
import result
import models.contentHouse as contentHouse
from marshmallow import Schema, fields, ValidationError
import json

#序列化
HouseSchema = contentHouse.HouseSchema()

class Connection(object):
    conn = None

    def __new__(cls, *args):
        if cls.conn is None:
            cls.conn = MongoClient(util.MONGO_HOST, port=util.MONGO_PORT, serverSelectionTimeoutMS=3000, connect=False)
        return cls.conn

def connect_collection(db_name, collection):
        result.write_log("info", "Connect to mongoDB, host: {0}, port: {1}, db: {2}, collection: {3}"
                         .format(util.MONGO_HOST, util.MONGO_PORT, db_name, collection))
        return Connection()[db_name][collection]

def store_houses():
        return connect_collection(util.MONGO_DB_ACCOUNT, util.MONGO_COLLECTION_ACCOUNT)

#---------------------------------------------------------------------------------------------------------------------------------

#
#尋找非屋主自行刊登物件
#
def houses_list():
    try:
        houses  = store_houses().find({'owner': {"$nin":['屋主']}})
        houses_data = HouseSchema.dump(houses, many=True)

        return houses_data
    except:
        result.write_log("critical", "Failed connect to mongoDB, method: houses_list")
        return None
#
#透過電話尋找租屋物件
#
def find_houses_by_phone_num(phone_num):
    try:
        house = store_houses().find_one({'phone_num': phone_num})
        house_data = HouseSchema.dump(house)
        return house_data

    except:
        result.write_log("critical", "Failed connect to mongoDB, method: find_houses_by_phone_num")
        return None
#
#透過地區和承租性別尋找租屋物件
#
def find_houses_by_gender_region(gender, region):
    try:
        house = store_houses().find({'addr': {'$regex': '^{}.*'.format(region)}, 'gender': gender}, {'name': 1, 'phone_num': 1, 'addr':1, 'gender':1})
        house_data = HouseSchema.dump(house, many=True)
        return house_data

    except:
        result.write_log("critical", "Failed connect to mongoDB, method: find_houses_by_phone_num")
        return None
#
#透過名字性別尋找符合房東之租屋物件
#
def find_houses_by_owner_region(name, region):
    try:
        house = store_houses().find({'name': name, 'addr': {'$regex': '^{}.*'.format(region)}}, {'name': 1, 'phone_num': 1, 'addr':1})
        house_data = HouseSchema.dump(house, many=True)
        return house_data

    except:
        result.write_log("critical", "Failed connect to mongoDB, method: find_houses_by_phone_num")
        return None

print(find_houses_by_owner_region('陳先生', '台北'))
