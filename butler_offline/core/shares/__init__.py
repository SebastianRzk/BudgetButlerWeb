
class SharesInfo:
    KOSTEN = 'Kosten'
    REGIONEN = 'Regionen'
    SEKTOREN = 'Sektoren'
    INDEX_NAME = 'IndexName'
    NAME = 'Name'
    _DATA_KEY = 'data'
    _NAME_KEY = 'name'
    _DATE_KEY = 'date'
    _SOURCE_KEY = 'source'
    changed = False
    content = {}
    
    def __init__(self, content):
        self.content = content
    
    def save(self, isin, date, source, data):
        if isin not in self.content:
            self.content = self.content | self._to_share_data(isin, date, source, data)
        else:
            self.content[isin][self._DATA_KEY].append(self._to_share_entry(date, source, data))
        self.changed = True
    
    def _to_share_data(self, isin, date, source, data):
        return {
                   isin: {
                       self._DATA_KEY: [
                            self._to_share_entry(date, source, data)
                           ]
                       }
                }

    def _to_share_entry(self, date, source, data):
        return {
                    self._DATE_KEY: date,
                    self._DATA_KEY: data,
                    self._SOURCE_KEY: source
                }

    def is_changed(self):
        return self.changed
    
    def get_latest_data_for(self, isin):
        if isin not in self.content:
            return None
        return self.content[isin][self._DATA_KEY][-1][self._DATA_KEY]
    
    def get_last_changed_date_for(self, isin):
        if isin not in self.content:
            return None
        return self.content[isin][self._DATA_KEY][-1][self._DATE_KEY]

    def filter_out_isins_without_data(self, isins):
        filtered = []
        for isin in isins:
            if self.get_latest_data_for(isin):
                filtered.append(isin)

        return filtered

