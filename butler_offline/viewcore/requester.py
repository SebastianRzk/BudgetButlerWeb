from butler_offline.viewcore import requester
import logging
import requests

INSTANCE = None

def instance():
    if not requester.INSTANCE:
        requester.INSTANCE = Requester()
    return requester.INSTANCE


class Requester:

    def get(self, server_url):
        logging.info('requested url %s', server_url)
        response = requests.get(server_url)
        logging.info(response, self.decode(response))
        response.raise_for_status()
        return self.decode(response)

    def post(self, server_url, data={}, cookies=None):
        logging.info('requested url %s', server_url, data)
        response = requests.post(server_url, data=data, cookies=cookies)
        response.raise_for_status()
        return self.decode(response)

    def decode(self, response):
        logging.info('response: %s', response)
        decoded_response = response.content.decode("utf-8")
        logging.info('decoded repsonse: %s', decoded_response)
        return decoded_response

    def post_raw(self, server_url, data):
        logging.info('requested url', server_url, data)
        response = requests.post(server_url, data=data)
        response.raise_for_status()
        return response

    def put(self, server_url, data, cookies):
        logging.info('requested url %s %s', server_url, data)
        response = requests.put(url=server_url, json=data, cookies=cookies)
        response.raise_for_status()
        return self.decode(response)
