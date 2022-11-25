from requests.exceptions import ConnectionError
import logging


class RequesterStub:
    def __init__(self, mocked_requests, mocked_decode='', auth_cookies=''):
        self.mocked_requests = mocked_requests
        self.call_count = {}
        self.mocked_decode = mocked_decode
        for url in mocked_requests.keys():
            self.call_count[url] = []
        self.auth_cookies = auth_cookies

    def post(self, url, data={}, cookies=None):
        logging.info('-----------------' + url)
        if url in self.mocked_requests:
            self.call_count[url].append(data)
            return self.mocked_requests[url]
        logging.error('WARNING, NON MATCHING REQUEST: %s %s', url, data)
        return None

    def get(self, url):
        logging.info('-----------------' + url)
        if url in self.mocked_requests:
            self.call_count[url].append('')
            return self.mocked_requests[url]
        logging.error('WARNING, NON MATCHING REQUEST: %s', url)
        return None

    def post_raw(self, url, data):
        return self.post(url, data)

    def put(self, url, data, cookies):
        if not self.auth_cookies == cookies:
            return 'error, auth not valid'
        return self.post(url, data)

    def decode(self, request):
        return self.mocked_decode

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
