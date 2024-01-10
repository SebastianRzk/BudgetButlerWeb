from butler_offline.viewcore import requester
import logging
import requests

INSTANCE = None


def instance():
    if not requester.INSTANCE:
        requester.INSTANCE = Requester()
    return requester.INSTANCE


class Requester:

    def get(self, server_url, cookies=None):
        logging.info('requested url %s', server_url)
        response = requests.get(server_url, cookies=cookies)
        logging.info("response: %s", response)
        logging.info("decoded reponse %s", self.decode(response))
        response.raise_for_status()
        return self.decode(response)

    def delete(self, server_url, cookies=None):
        logging.info('requested url %s', server_url)
        response = requests.delete(server_url, cookies=cookies)
        logging.info("response: %s", response)
        logging.info("decoded reponse %s", self.decode(response))
        response.raise_for_status()
        return self.decode(response)


    def post(self, server_url, data: dict = None, cookies=None):
        if not data:
            data = {}
        logging.info('requested url for post %s', server_url)
        logging.info("data %s", data)
        logging.info("cookies %s", cookies)
        response = requests.post(url=server_url, json=data, cookies=cookies)
        response.raise_for_status()
        return self.decode(response)

    def decode(self, response):
        logging.info('response: %s', response)
        decoded_response = response.content.decode("utf-8")
        logging.info('decoded repsonse: %s', decoded_response)
        return decoded_response

    def post_raw(self, server_url, data):
        logging.info('requested url %s', server_url)
        response = requests.post(server_url, data=data)
        response.raise_for_status()
        return response
