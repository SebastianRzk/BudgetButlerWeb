from butler_offline.viewcore import requester
from butler_offline.online_services.butler_online.online_routes import SET_KATEOGIEN_URL


def set_kategorien(server_url, kategorien, auth_container):
    requester.instance().post(SET_KATEOGIEN_URL.format(server_url=server_url),
                              data={'kategorien': kategorien},
                              cookies=auth_container.cookies())
