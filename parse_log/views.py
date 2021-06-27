from settings import settings as st
from .models import ReadLog


class ParseLog(object):
    def __init__(self, path=st.APACHE_LOG_PATH):
        self.read_log = ReadLog(path)
        self.log_data = []

    def parse_log(self):
        """
        解析log日志
        :return:
        """
        self.log_data = self.read_log.read()
        return self.log_data

    def insert_db(self, db_coll):
        return db_coll.insert_many(self.log_data)

