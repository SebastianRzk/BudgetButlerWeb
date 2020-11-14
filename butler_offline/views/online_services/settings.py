from butler_offline.viewcore import requester


def set_kategorien(serverurl, kategorien, auth_container):
    serverurl = serverurl + '/setkategorien.php'
    requester.instance().post(serverurl, data={'kategorien': kategorien}, cookies=auth_container.cookies())
