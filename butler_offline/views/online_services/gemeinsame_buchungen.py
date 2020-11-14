from butler_offline.viewcore import requester
import json


def get_gemeinsame_buchungen(serverurl, auth_container):
    json_data = requester.instance().post(serverurl + '/gemeinsamebuchung.php',
                                          cookies=auth_container.cookies())
    return json.loads(json_data)


def upload_gemeinsame_buchungen(serverurl, data, auth_container):
    json_data = requester.instance().put(serverurl + '/gemeinsamebuchung.php', data, auth_container.cookies())
    return json.loads(json_data)['result'] == 'OK'


def delete_gemeinsame_buchungen(serverurl, auth_container):
    requester.instance().post(serverurl + '/deletegemeinsam.php', cookies=auth_container.cookies())

