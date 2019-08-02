from butler_offline.core.export.StringWriter import StringWriter


class TextReport:

    def generate_report(self, dataframe, headline=''):
        textreport = StringWriter()

        textreport.write_line(headline)
        textreport.write_empty_line(count=1)
        textreport.write_line('#######MaschinenimportStart')
        textreport.write(dataframe.to_csv(index=False))
        textreport.write_line('#######MaschinenimportEnd')

        return textreport.to_string()


        
