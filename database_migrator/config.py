import configuration_provider

DEFAULT_CONFIG = {
    "database_configuration": {
        "name": "Test_User",
        "location": "data"
    },
    "design_configuration": {
        "configurierte_farben": [
            {
                "as_string": "#1a5fb4"
            },
            {
                "as_string": "#26a269"
            },
            {
                "as_string": "#e5a50a"
            },
            {
                "as_string": "#c64600"
            },
            {
                "as_string": "#a51d2d"
            },
            {
                "as_string": "#613583"
            },
            {
                "as_string": "#63452c"
            },
            {
                "as_string": "#9a9996"
            },
            {
                "as_string": "#000000"
            },
            {
                "as_string": "#99c1f1"
            },
            {
                "as_string": "#8ff0a4"
            },
            {
                "as_string": "#f9f06b"
            },
            {
                "as_string": "#ffbe6f"
            },
            {
                "as_string": "#f66151"
            },
            {
                "as_string": "#dc8add"
            },
            {
                "as_string": "#cdab8f"
            },
            {
                "as_string": "#ffffff"
            },
            {
                "as_string": "#77767b"
            }
        ],
        "design_farbe": {
            "as_string": "#1c71d8"
        }
    },
    "user_configuration": {
        "self_name": {
            "person": "Test_User"
        },
        "partner_name": {
            "person": "kein_Partnername_gesetzt"
        }
    },
    "abrechnungs_configuration": {
        "location": "data/abrechnungen"
    },
    "backup_configuration": {
        "location": "data/backups",
        "import_backup_location": "data/backups/import_backup"
    },
    "server_configuration": {
        "server_url": "http://localhost"
    },
    "erfassungs_configuration": {
        "ausgeschlossene_kategorien": [
            {
                "kategorie": "adda"
            },
            {
                "kategorie": "asd"
            }
        ]
    }
}

def get_applied_configuration():
    self_name = configuration_provider.get_configuration('DATABASES')
    if ',' in self_name:
        self_name = self_name.split(',')[0]
    partner_name = configuration_provider.get_configuration('PARTNERNAME')
    online_default_server = configuration_provider.get_configuration('ONLINE_DEFAULT_SERVER')
    ausgeschlossene_kartgorien = configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN').split(',')

    conf = DEFAULT_CONFIG

    conf['database_configuration']['name'] = self_name
    ausgeschlossene_kartgorien_liste = []
    for kategorie in ausgeschlossene_kartgorien:
        if kategorie:
            ausgeschlossene_kartgorien_liste.append({'kategorie': kategorie})
    conf['erfassungs_configuration']['ausgeschlossene_kategorien'] = ausgeschlossene_kartgorien_liste

    conf['user_configuration']['self_name']['person'] = self_name
    conf['user_configuration']['partner_name']['person'] = partner_name

    conf['server_configuration']['server_url'] = online_default_server

    return conf



