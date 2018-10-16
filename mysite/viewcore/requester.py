from mysite.viewcore import requester
import requests

INSTANCE = None

def instance():
    if not requester.INSTANCE:
        requester.INSTANCE = Requester()
    return requester.INSTANCE


class Requester:

    def post(self, serverurl, data):
        response = requests.post(serverurl, data=data)
        decoded_response = response.content.decode("utf-8")
        print('decoded repsonse:', decoded_response)
        return decoded_response
