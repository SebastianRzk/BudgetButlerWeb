
from butler_offline.core.export.json_report import JSONReport
from butler_offline.core.export.text_report import TextReportWriter

class JSONToTextMapper:

    def map(self, json):
        dataframe = JSONReport().dataframe_from_json(json)
        return TextReportWriter().generate_report(dataframe)

    def map_gemeinsam(self, json):
        dataframe = JSONReport().dataframe_from_json_gemeinsam(json)
        return TextReportWriter().generate_report(dataframe)

