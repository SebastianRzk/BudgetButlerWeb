from mysite.viewcore import requester

INSTANCE = None

def instance():
    if not requester.INSTANCE:
        requester.INSTANCE = Requester()
    return requester.INSTANCE


class Requester:

    def post(serverurl, data):
        response = requests.post(serverurl, data=data)
        return response.content.decode("utf-8")
        
