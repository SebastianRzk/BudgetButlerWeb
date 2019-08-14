from butler_offline.viewcore import requester
import json


def get_einzelbuchungen(serverurl, email, password):
    jsondata = requester.instance().post(serverurl + '/einzelbuchung.php', data={'email': email, 'password': password})
    return json.loads(jsondata)
