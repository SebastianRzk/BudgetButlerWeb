from viewcore import viewcore
from viewcore.viewcore import post_action_is
from viewcore import request_handler
from viewcore import configuration_provider
from importd import views as importview
import requests
from test.RequestStubs import PostRequest
from test import RequestStubs

def _handle_request(request):
    if post_action_is(request, 'edit_databases'):
        dbs = request.POST['dbs']
        configuration_provider.set_configuration('DATABASES', dbs)
        viewcore.DATABASES = []
        viewcore.DATABASE_INSTANCE = None

    if post_action_is(request, 'add_kategorie'):
        viewcore.database_instance().einzelbuchungen.add_kategorie(request.POST['neue_kategorie'])

    if post_action_is(request, 'change_themecolor'):
        configuration_provider.set_configuration('THEME_COLOR', request.POST['themecolor'])

    if post_action_is(request, 'set_kategorien'):
        kategorien = ','.join(sorted(viewcore.database_instance().einzelbuchungen.get_kategorien_ausgaben()))
        serverurl = request.POST['server'] + '/setkategorien.php'

        if not serverurl.startswith('http://') or serverurl.startswith('https://'):
             serverurl = 'https://' + serverurl

        r = requests.post(serverurl, data={'email': request.POST['email'], 'password': request.POST['password'], 'kategorien': kategorien})

    if post_action_is(request, 'load_online_transactions'):
        serverurl = request.POST['server'] +

        if not serverurl.startswith('http://') or serverurl.startswith('https://'):
             serverurl = 'https://' + serverurl

        r = requests.post(serverurl + '/getabrechnung.php', data={'email': request.POST['email'], 'password': request.POST['password']})
        print(r.content)
        _write_to_file("../Online_Import/Import_" + str(datetime.now()), r.content)

        RequestStubs.CONFIGURED = True
        importview.handle_request(PostRequest({'import' : r.content.decode("utf-8")}))
        r = requests.post(serverurl + '/deleteitems.php', data={'email': request.POST['email'], 'password': request.POST['password']})

    if post_action_is(request, 'change_colorpalette'):
        request_colors = []
        for colornumber in range(0, 20):
            if str(colornumber) + '_checked' in request.POST:
                request_colors.append(request.POST[str(colornumber) + '_farbe'][1:])
        configuration_provider.set_configuration('DESIGN_COLORS', ','.join(request_colors))

    if post_action_is(request, 'set_partnername'):
        viewcore.database_instance().gemeinsamebuchungen.rename(viewcore.name_of_partner(), request.POST['partnername'])
        configuration_provider.set_configuration('PARTNERNAME', request.POST['partnername'])

    farbmapping = []
    for colornumber in range(0, 20):
        checked = False
        kategorie = 'keine'
        color = viewcore.design_colors()[colornumber % len(viewcore.design_colors())]
        len_kategorien = len(viewcore.database_instance().einzelbuchungen.get_alle_kategorien())
        if colornumber < len_kategorien:
            kategorie = list(viewcore.database_instance().einzelbuchungen.get_alle_kategorien())[colornumber % len_kategorien]
        if colornumber < len(viewcore.design_colors()):
            checked = True

        farbmapping.append({
            'nummer': colornumber,
            'checked': checked,
            'farbe' : color,
            'kategorie' : kategorie
            })

    context = viewcore.generate_base_context('configuration')
    context['palette'] = farbmapping
    default_databases = ''
    for db in viewcore.DATABASES:
        if len(default_databases) != 0:
            default_databases = default_databases + ','
        default_databases = default_databases + db
    context['default_databases'] = default_databases
    context['partnername'] = viewcore.name_of_partner()
    context['themecolor'] = configuration_provider.get_configuration('THEME_COLOR')
    context['transaction_key'] = 'requested'
    return context



def _write_to_file(self, filename, content):
    f = open(filename, "w")
    f.write(content)


def index(request):
    return request_handler.handle_request(request, _handle_request, 'konfiguration.html')

