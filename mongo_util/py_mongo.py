from __future__ import unicode_literals
from pymongo import MongoClient

from settings import settings


class ApacheLogModel(object):
    """
    mongodb单例模式
    """

    def __init__(self, db_coll):
        """
        这里第一个参数是cls， 表示调用当前的类名
        :return:
        """
        self.__coll = None
        if not self.__coll:
            self.conn(db_coll)

    def conn(self, db_coll):
        client = MongoClient(settings.MONGO_URL)
        db = client["test_db"]
        self.__coll = db[db_coll]

    def insert_one(self, insert_data):
        return self.__coll.insert_one(insert_data)

    def insert_many(self, insert_data_list):
        return self.__coll.insert_many(insert_data_list)

    def find_one(self, query_filter):
        return self.__coll.find_one(query_filter)

    def aggregate_data(self, pipeline):
        return self.__coll.aggregate(pipeline=pipeline)
