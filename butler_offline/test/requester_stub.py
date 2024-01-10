from requests.exceptions import ConnectionError
import logging


class RequesterStub:
    def __init__(self, mocked_requests):
        self.mocked_requests = mocked_requests
        self.call_count = {}
        for url in mocked_requests.keys():
            self.call_count[url] = []

    def post(self, url, data: dict | None = None, cookies=None):
        if not data:
            data = {}
        logging.info('-----------------' + url)
        if url in self.mocked_requests:
            self.call_count[url].append(data)
            return self.mocked_requests[url]
        logging.error('ERROR, NON MATCHING REQUEST: %s %s', url, data)
        return None

    def delete(self, url, data: dict | None = None, cookies=None):
        if not data:
            data = {}
        logging.info('-----------------' + url)
        if url in self.mocked_requests:
            self.call_count[url].append(data)
            return self.mocked_requests[url]
        logging.error('ERROR, NON MATCHING REQUEST: %s %s', url, data)
        return None

    def get(self, url, cookies=None):
        logging.info('-----------------' + url)
        if url in self.mocked_requests:
            self.call_count[url].append('')
            return self.mocked_requests[url]
        logging.error('ERROR, NON MATCHING REQUEST: %s', url)
        return None

    def post_raw(self, url, data):
        return self.post(url, data)

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


class RequesterErrorStub:
    def post(self, url, data):
        raise ConnectionError('Just for the test')

    def post_raw(self, url, data):
        return self.post(url, data)


class MockedResponse:
    def __init__(self, data, cookies):
        self.data = data
        self.cookies = cookies
