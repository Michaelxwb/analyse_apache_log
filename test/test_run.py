from analyse_log.views import AnalyseLogData
from report_form.views import ReportForm
from parse_log.views import ParseLog


class TestCase(object):
    """
    在根目录，在命令行中使用pytest进行测试
    """
    def test_parse_log(self):
        """ 用例， 解析log """
        assert ParseLog().parse_log() != False

    def test_article_title(self):
        """ 用例， 获取文件名 """
        log_data = {}
        assert AnalyseLogData(log_data).analyse() != False

    def test_analyse_log(self):
        """ 用例， 分析log """
        # 解析日志
        log_data = ParseLog().parse_log()

        # 分析日志
        analyse_data = AnalyseLogData(log_data).analyse()

        # 生成报表
        ReportForm(analyse_data=analyse_data, type="mk", article_title_dict=log_data["article_title_dict"]).write_form()

