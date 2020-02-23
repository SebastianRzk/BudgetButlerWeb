from butler_offline.viewcore import requester
import json


def get_gemeinsame_buchungen(serverurl, email, password):
    json_data = requester.instance().post(serverurl + '/gemeinsamebuchung.php',
                                          data={'email': email, 'password': password})
    return json.loads(json_data)


def upload_gemeinsame_buchungen(serverurl, data, auth_container):
    json_data = requester.instance().put(serverurl + '/gemeinsamebuchung.php', data, auth_container.cookies())
    return json.loads(json_data)['result'] == 'OK'
