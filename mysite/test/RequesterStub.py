class RequesterStub:
    def __init__(self, mocked_requests):
        self.mocked_requests = mocked_requests
        self.call_count = {}
        for url in mocked_requests.keys():
            self.call_count[url] = []

    def post(self, url, data):
        print('-----------------',url)
        if url in self.mocked_requests:
            self.call_count[url].append(data)
            return self.mocked_requests[url]
        return None

    def call_count_of(self, url):
        if url not in self.call_count:
            return 0
        return len(self.call_count[url])

    def complete_call_count(self):
        count = 0
        for value in self.call_count.values():
            count += len(value)
        return count

    def data_of_request(self, url):
        if url not in self.call_count:
            return None
        return self.call_count[url]


from requests.exceptions import ConnectionError

class RequesterErrorStub:
    def post(self, url, data):
        raise ConnectionError('Just for the test')

