from butler_offline.viewcore import requester
import json


def get_einzelbuchungen(serverurl, auth_container):
    jsondata = requester.instance().post(serverurl + '/einzelbuchung.php', cookies=auth_container.cookies())
    return json.loads(jsondata)

def delete_einzelbuchungen(serverurl, auth_container):
    requester.instance().post(
        serverurl + '/deleteitems.php',
        cookies=auth_container.cookies()
      )
