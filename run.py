import time

from analyse_log.views import AnalyseLogData
from mongo_util.py_mongo import ApacheLogModel
from parse_log.views import ParseLog
from report_form.views import ReportForm
from settings import settings


def parsing_data(db_coll):
    """
    解析日志入库
    :param db_coll:
    :return:
    """
    # 解析日志
    parse_log = ParseLog()
    log_data = parse_log.parse_log()
    if not log_data:
        return None

    return parse_log.insert_db(db_coll)


def generate_table(db_coll):
    """
    生成报表
    :param db_coll:
    :return:
    """
    # 分析日志
    analyse_data = AnalyseLogData(db_coll).analyse()
    # 生成报表
    ReportForm(analyse_data=analyse_data, type="mk", article_title_dict={}).write_form()


if __name__ == '__main__':
    stime = time.time()
    al_coll = ApacheLogModel(settings.DB_NAME)
    ret = parsing_data(al_coll)
    if ret:
        generate_table(al_coll)
    print("user_time = {}".format(time.time() - stime))
