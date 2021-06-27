import logging
import traceback

from settings import settings as st


class MKForm(object):
    """
    markdown表格
    """

    def __init__(self, article_title_dict=None):
        self.article_title_dict = article_title_dict

    def write_markdown_form(self, header_list, data, path, source=None):
        """
        生成markdown表格
        :param header_list:
        :param data:
        :param path:
        :param source:
        :return:
        """
        if not header_list:
            logging.error("header_list = {}".format(header_list))
            return False

        header = ""
        row_format = ""
        for item, index in enumerate(range(len(header_list))):
            # {{ 转义 {
            header += '| {{0[{}]}} '.format(index)
            row_format += '| {{0[{}]}} '.format(index)
        header += "|\n"
        row_format += "|\n"
        header = header.format(header_list)
        header_format = "| --- " * len(header_list) + "|\n"

        with open(path, "w") as f:
            # 写入表头
            f.write(header)
            f.write(header_format)

            # 判断来源获取标题字典
            if source != st.ARTICLE_FORMAT:
                for item_list in data:
                    try:
                        f.write(row_format.format(item_list))
                    except Exception:
                        logging.error(traceback.format_exc())
            else:
                for item_list in data:
                    article_title = self.article_title_dict.get(item_list[0], "")
                    item_list = list(item_list)
                    item_list.insert(1, article_title)
                    try:
                        f.write(row_format.format(item_list))
                    except Exception:
                        logging.error(traceback.format_exc())
        return True
