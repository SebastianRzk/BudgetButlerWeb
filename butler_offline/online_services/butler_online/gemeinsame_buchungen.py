import json
import logging

from butler_offline.online_services.butler_online.online_routes import GEMEINSAMEBUCHUNGEN_URL, \
    GEMEINSAMEBUCHUNGEN_BATCH_UPLOAD_URL
from butler_offline.viewcore import requester


def get_gemeinsame_buchungen(server_url, auth_container):
    json_data = requester.instance().get(GEMEINSAMEBUCHUNGEN_URL.format(server_url=server_url),
                                         cookies=auth_container.cookies())
    return json.loads(json_data)


def upload_gemeinsame_buchungen(server_url, data, auth_container):
    json_data = requester.instance().post(GEMEINSAMEBUCHUNGEN_BATCH_UPLOAD_URL.format(server_url=server_url),
                                          data,
                                          auth_container.cookies())
    logging.info("Result upload %s", json_data)
    return json.loads(json_data)['result'] == 'OK'


def delete_gemeinsame_buchungen(server_url, auth_container):
    requester.instance().delete(GEMEINSAMEBUCHUNGEN_URL.format(server_url=server_url),
                                cookies=auth_container.cookies())
