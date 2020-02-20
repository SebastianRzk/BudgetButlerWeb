from butler_offline.viewcore import requester
import json

def get_username(serverurl, email, password):
    auth_container_string = requester.instance().post(serverurl + '/login.php', data={'email': email, 'password': password})
    auth_container = json.loads(auth_container_string)
    return auth_container['username']

def get_partnername(serverurl, email, password):
    partner_configuration_string = requester.instance().post(serverurl + '/partner.php', data={'email': email, 'password': password})
    partner_configuration = json.loads(partner_configuration_string)
    return partner_configuration['partnername']
