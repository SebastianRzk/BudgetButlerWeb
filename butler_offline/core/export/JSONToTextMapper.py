
from butler_offline.core.export.JSONReport import JSONReport
from butler_offline.core.export.TextReport import TextReport

class JSONToTextMapper:

    def map(self, json_as_string):
        dataframe = JSONReport().dataframe_from_json_string(json_as_string)
        return TextReport().generate_report(dataframe)
