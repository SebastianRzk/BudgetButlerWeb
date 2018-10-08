class RequesterStub:
    def __init__(self, mocked_requests):
        self.mocked_requests = mocked_requests
        self.call_count = {}
        for url in mocked_requests.keys():
            self.call_count[url] = 0

    def post(self, url, data):
        print('-----------------',url)
        if url in self.mocked_requests:
            self.call_count[url] = self.call_count[url] + 1
            return self.mocked_requests[url]
        return None

    def call_count_of(self, url):
        if url not in self.call_count:
            return 0
        return self.call_count[url]

    def complete_call_count(self):
        return sum(self.call_count.values())
