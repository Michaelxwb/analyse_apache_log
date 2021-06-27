from .models import MKForm


class ReportForm(object):
    def __init__(self, **kwargs):
        self.article_title_dict = kwargs.get("article_title_dict")
        self.analyse_data = kwargs.get("analyse_data")
        self.type = kwargs.get("type")

    def write_form(self):
        """
        生成表格
        :return:
        """
        # 生成markdown报表
        if self.type == "mk":
            mk_form = MKForm(article_title_dict=self.article_title_dict)
            for value in self.analyse_data.values():
                mk_form.write_markdown_form(value.get("header"), value.get("analyse_value"),
                                            value.get("path"), value.get("source"))
        else:
            return None

        return True
