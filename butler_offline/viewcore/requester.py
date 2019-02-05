from butler_offline.viewcore import requester
import requests

INSTANCE = None

def instance():
    if not requester.INSTANCE:
        requester.INSTANCE = Requester()
    return requester.INSTANCE


class Requester:

    def post(self, serverurl, data):
        response = requests.post(serverurl, data=data)
        response.raise_for_status()
        decoded_response = response.content.decode("utf-8")
        print('decoded repsonse:', decoded_response)
        return decoded_response
