
from butler_offline.core.export.JSONReport import JSONReport
from butler_offline.core.export.TextReport import TextReport

class JSONToTextMapper:

    def map(self, json):
        dataframe = JSONReport().dataframe_from_json(json)
        return TextReport().generate_report(dataframe)

    def map_gemeinsam(self, json):
        dataframe = JSONReport().dataframe_from_json_gemeinsam(json)
        return TextReport().generate_report(dataframe)

