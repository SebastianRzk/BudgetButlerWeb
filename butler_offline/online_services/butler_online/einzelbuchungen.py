import json
import logging

from butler_offline.online_services.butler_online.online_routes import EINZELBUCHUNGEN_URL
from butler_offline.viewcore import requester


def get_einzelbuchungen(server_url, auth_container):
    json_data = requester.instance().get(
        EINZELBUCHUNGEN_URL.format(server_url=server_url), cookies=auth_container.cookies())
    return json.loads(json_data)


def delete_einzelbuchungen(server_url, auth_container):
    requester.instance().delete(
        EINZELBUCHUNGEN_URL.format(server_url=server_url),
        cookies=auth_container.cookies()
    )
