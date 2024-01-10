from butler_offline.online_services.butler_online.online_routes import SET_KATEGORIEN_BATCH_URL,KATEGORIEN_URL
from butler_offline.viewcore import requester


def set_kategorien(server_url, kategorien, auth_container):
    requester.instance().post(SET_KATEGORIEN_BATCH_URL.format(server_url=server_url),
                              data=kategorien,
                              cookies=auth_container.cookies())


def delete_kategorien(server_url, auth_container):
    requester.instance().delete(KATEGORIEN_URL.format(server_url=server_url),
                                cookies=auth_container.cookies())
