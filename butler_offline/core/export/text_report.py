from butler_offline.core.export.StringWriter import StringWriter
import pandas
from _io import StringIO


class TextReportWriter:

    def generate_report(self, dataframe, headline=''):
        textreport = StringWriter()

        textreport.write_line(headline)
        textreport.write_empty_line(count=1)
        textreport.write_line('#######MaschinenimportStart')
        textreport.write(dataframe.to_csv(index=False))
        textreport.write_line('#######MaschinenimportEnd')

        return textreport.to_string()



class TextReportReader:
    def read(self, content):
        tables = {}
        tables["sonst"] = ""
        tables["#######MaschinenimportStart"] = ""
        mode = "sonst"
        print('textfield content:', content)
        for line in content.split('\n'):
            print(line)
            line = line.strip()
            if line == "":
                continue
            if line == "#######MaschinenimportStart":
                mode = "#######MaschinenimportStart"
                continue

            if line == "#######MaschinenimportEnd":
                mode = "sonst"
                continue
            tables[mode] = tables[mode] + "\n" + line

        print(tables)

        return pandas.read_csv(StringIO(tables["#######MaschinenimportStart"]))
