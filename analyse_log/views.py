import logging
import traceback

from settings import settings as st


class AnalyseLogData(object):
    """
    分析log日志
    """

    def __init__(self, db_coll):
        """
        :param db_coll:
        """
        self.db_coll = db_coll

    def analyse(self):
        """
        分析数据
        :return:
        """
        analyse_data = {}

        # 文章报表
        article_analyse_value = self.analyse_article_report()
        analyse_data["article_analyse"] = {
            "header": st.ARTICLE_HEADER_LIST,
            "path": st.ARTICLE_FORMAT_PATH,
            "source": st.ARTICLE_FORMAT,
            "analyse_value": article_analyse_value,
        }

        # IP报表
        ip_analyse_value = self.analyse_ip_report()
        analyse_data["article_ip"] = {
            "header": st.IP_HEADER_LIST,
            "path": st.IP_FORMAT_PATH,
            "source": st.IP_FORMAT,
            "analyse_value": ip_analyse_value,
        }

        # 完整报表
        complete_analyse_value = self.analyse_complete_report()
        analyse_data["article_complete"] = {
            "header": st.COMPLETE_HEADER_LIST,
            "path": st.COMPLETE_FORMAT_PATH,
            "source": st.COMPLETE_FORMAT,
            "analyse_value": complete_analyse_value,
        }

        return analyse_data

    def analyse_ip_report(self):
        """
        分析IP报表
        :return:
        """
        pipeline = [
            {"$match": {"is_deleted": 0, "url_suffix": {"$in": st.ARTICLE_EX}, "resp_code": 200}},
            {"$group": {
                "_id": "$ip",
                "url_list": {"$push": "$req_url"},
                "count": {"$sum": 1}}}
        ]
        try:
            ret = self.db_coll.aggregate_data(pipeline)
            if ret is False:
                logging.error("get data fail, pipeline = {}".format(pipeline))
                return False
            ip_count_values = [[item["_id"], item["count"], len(set(item["url_list"]))] for item in ret]
            # 从pandas表格转化成普通的列表数据
            return ip_count_values
        except Exception:
            logging.error(traceback.format_exc())

    def analyse_article_report(self):
        """
        分析文章报表
        :return:
        """
        pipeline = [
            {"$match": {"is_deleted": 0, "url_suffix": {"$in": st.ARTICLE_EX}, "resp_code": 200}},
            {"$group": {
                "_id": "$req_url",
                "ip_list": {"$push": "$ip"},
                "count": {"$sum": 1}}}
        ]
        try:
            ret = self.db_coll.aggregate_data(pipeline)
            if ret is False:
                logging.error("get data fail, pipeline = {}".format(pipeline))
                return False
            request_count_values = [[item["_id"], item["count"], len(set(item["ip_list"]))] for item in ret]
            return request_count_values
        except Exception:
            logging.error(traceback.format_exc())

    def analyse_complete_report(self):
        """
        分析完整报表
        :return:
        """
        pipeline = [
            {"$match": {"is_deleted": 0, "url_suffix": {"$in": st.ARTICLE_EX}, "resp_code": 200}},
            {"$group": {
                "_id": {"req_url": "$req_url", "ip": "$ip"},
                "count": {"$sum": 1}}}
        ]
        try:
            ret = self.db_coll.aggregate_data(pipeline)
            if ret is False:
                logging.error("get data fail, pipeline = {}".format(pipeline))
                return False
            request_count_values = [[item["_id"]["ip"], item["_id"]["req_url"], item["count"]] for item in ret]
            return request_count_values
        except Exception:
            logging.error(traceback.format_exc())
