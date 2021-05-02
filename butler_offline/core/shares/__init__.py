
class SharesInfo:
    _DATA_KEY = 'data'
    _NAME_KEY = 'name'
    _DATE_KEY = 'date'
    _SOURCE_KEY = 'source'
    changed = False
    content = {}
    
    def __init__(self, content):
        self.content = content
    
    def save(self, isin, date, source, data):
        self.content = self.content | self._get_share_data(isin, date, source, data)
        self.changed = True
    
    def _get_share_data(self, isin, date, data, source):
        return {
                   isin: {
                       self._DATA_KEY: [
                            {
                                self._DATE_KEY: date,
                                self._DATA_KEY: data,
                                self._SOURCE_KEY: source
                                }
                           ]
                       }
                }
        
        
    def is_changed(self):
        return self.changed
    
    def get_latest_data_for(self, isin):
        if isin not in self.content:
            return None
        if not len(self.content[isin][self._DATA_KEY]):
            return None
        return self.content[isin][self._DATA_KEY][0][self._DATA_KEY]
    
    def get_last_changes_for(self, isin):
        if isin not in self.content:
            return None
        if not len(self.content[isin][self._DATA_KEY]):
            return None
        return self.content[isin][self._DATA_KEY][0][self._DATE_KEY]
