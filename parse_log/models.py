import datetime
import re
import os
import logging
import traceback

from settings import settings as st

# log日志正则
log_pattern = re.compile(st.APACHE_LOG_RE)


class ReadLog(object):
    def __init__(self, path):
        self.path = path
        self.log_data = []

    def read(self):
        """
        读取日志
        :return:
        """
        if not os.path.exists(self.path):
            logging.error("path exists = {}".format(self.path))
            return False

        # 获取文件夹下的文件列表， 只获取.log文件
        filenames = [item for item in os.listdir(self.path) if os.path.splitext(item)[1] == '.log']
        time_stamp = 1624698910000
        for filename in filenames:
            file_path = "{}/{}".format(self.path, filename)
            with open(file_path, mode="r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    self.parse(line, time_stamp)

        return self.log_data

    def parse(self, line, time_stamp):
        """
        解析单行apache日志
        :param line:
        :param time_stamp:
        :return:
        """
        result = log_pattern.match(line)
        if not result:
            logging.error(f"re error, line = {line}")
            return False

        data_dict = {}
        try:
            # ip处理
            ip = result.group("ip")
            if ip.strip() == '-' or ip.strip() == "":  # 如果是匹配到没有ip就把这条数据丢弃
                logging.warning("ip is None!, line = {}".format(line))
                return False
            data_dict['ip'] = ip

            # request_url处理
            request = result.group("request")
            request_list = request.split()
            url_name = request_list[1].split("?")[0]  # 往往url后面会有一些参数，取出不带参数的url

            # 获取后缀
            extension = url_name.rsplit(".")[-1]
            if extension in st.FILTER_EX:
                return False
            data_dict["req_meth"] = request_list[0]
            data_dict["req_url"] = url_name
            data_dict["url_suffix"] = extension

            # 时间处理
            time = result.group("time")  # 21/Dec/2019:21:45:31 +0800
            time = time.replace(" +0800", "")  # 替换+0800为空
            t = datetime.datetime.strptime(time, "%d/%b/%Y:%H:%M:%S")  # 将时间格式化成友好的格式
            data_dict['access_time'] = str(t)

            # 状态码处理
            data_dict['resp_code'] = int(result.group("status")) if result.group("status") else ""
            data_dict["is_deleted"] = 0
            data_dict["create_time"] = time_stamp
            data_dict["update"] = time_stamp
            self.log_data.append(data_dict)

        except Exception:
            logging.error(traceback.format_exc())
            return False
