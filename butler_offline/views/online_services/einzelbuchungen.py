from butler_offline.viewcore import requester
import json


def get_einzelbuchungen(serverurl, auth_container):
    jsondata = requester.instance().post(serverurl + '/einzelbuchung.php', cookies=auth_container.cookies())
    return json.loads(jsondata)
