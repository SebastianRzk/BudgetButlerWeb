import datetime

from butler_offline.core import configuration_provider
from butler_offline.core.configuration_provider import ConfigurationProvider
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context, PageContext
from butler_offline.viewcore.converter import datum
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.viewcore.converter import datum_to_string
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import gemeinsame_buchung_needed_decorator


class AbrechnenVorschauContext:
    def __init__(self,
                 name: str,
                 gemeinsamebuchungen: Gemeinsamebuchungen,
                 einzelbuchungen: Einzelbuchungen,
                 configuration: ConfigurationProvider
                 ):
        self._name = name
        self._gemeinsamebuchungen = gemeinsamebuchungen
        self._einzelbuchungen = einzelbuchungen
        self._configuration = configuration

    def name(self) -> str:
        return self._name

    def gemeinsamebuchungen(self) -> Gemeinsamebuchungen:
        return self._gemeinsamebuchungen

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen

    def configuration(self) -> ConfigurationProvider:
        return self._configuration


@gemeinsame_buchung_needed_decorator()
def handle_request(request: Request, context: AbrechnenVorschauContext):
    result_context = generate_transactional_page_context('gemeinsamabrechnen')

    name_self = context.name()
    name_partner = context.configuration().get_configuration('PARTNERNAME')

    mindate = context.gemeinsamebuchungen().min_date()
    maxdate = context.gemeinsamebuchungen().max_date()

    set_mindate = request.get_post_parameter_or_default('set_mindate', mindate, mapping_function=datum)
    set_maxdate = request.get_post_parameter_or_default('set_maxdate', maxdate, mapping_function=datum)
    selector = context.gemeinsamebuchungen().select().select_range(set_mindate, set_maxdate)

    replay_value_if_defined(result_context, 'set_verhaeltnis', request, default=50)
    set_verhaeltnis = int(result_context.get('set_verhaeltnis'))
    replay_value_if_defined(result_context, 'set_limit', request)
    replay_value_if_defined(result_context, 'set_limit_value', request, default=50)
    replay_value_if_defined(result_context, 'set_limit_fuer', request)
    replay_value_if_defined(result_context, 'set_self_kategorie', request)
    replay_value_if_defined(result_context, 'set_self_kategorie_value', request)
    replay_value_if_defined(result_context, 'set_other_kategorie', request)
    replay_value_if_defined(result_context, 'set_other_kategorie_value', request, 'Korrekturbuchung')

    select_self = selector.fuer(name_self)
    select_partner = selector.fuer(name_partner)
    ausgabe_self = select_self.sum()
    ausgabe_partner = select_partner.sum()
    ausgabe_gesamt = selector.sum()

    ergebnis = ''

    if set_verhaeltnis != 50:
        ergebnis += '{self_name} übernimmt einen Anteil von {verhaeltnis}% der Ausgaben.<br>'.format(
            self_name=name_self, verhaeltnis=set_verhaeltnis)

    if request.is_post_parameter_set('set_limit'):
        ergebnis_satz = '''Durch das Limit bei {name} von {limit_value} EUR wurde das ''' + \
                        '''Verhältnis von {verhaeltnis_alt} auf {verhaeltnis_neu} aktualisiert<br>'''
        verhaeltnis_alt = set_verhaeltnis
        limited_person = request.values['set_limit_fuer']
        limit_value = int(request.values['set_limit_value'])

        if limited_person == name_partner:
            partner_soll = abs(ausgabe_gesamt * ((100 - set_verhaeltnis) / 100))
            if partner_soll > limit_value:
                set_verhaeltnis = 100 - abs((limit_value / ausgabe_gesamt) * 100)
                ergebnis += ergebnis_satz.format(name=name_partner, limit_value=limit_value,
                                                 verhaeltnis_alt=verhaeltnis_alt, verhaeltnis_neu=set_verhaeltnis)
        else:
            self_soll = abs(ausgabe_gesamt * (set_verhaeltnis / 100))
            if self_soll > limit_value:
                set_verhaeltnis = abs((limit_value / ausgabe_gesamt) * 100)
                ergebnis += ergebnis_satz.format(name=name_self, limit_value=limit_value,
                                                 verhaeltnis_alt=verhaeltnis_alt, verhaeltnis_neu=set_verhaeltnis)

    self_soll = (ausgabe_gesamt * (set_verhaeltnis / 100))
    self_diff = self_soll - ausgabe_self
    partner_soll = (ausgabe_gesamt * ((100 - set_verhaeltnis) / 100))
    partner_diff = partner_soll - ausgabe_partner

    ergebnis_satz = 'Die gemeinsamen Ausgaben sind ausgeglichen.'
    if partner_diff > 0 or self_diff < 0:
        ergebnis_satz = name_partner + ' bekommt von ' + name_self + ' noch ' + str('%.2f' % partner_diff) + '€.'

    if self_diff > 0 or partner_diff < 0:
        ergebnis_satz = name_self + ' bekommt von ' + name_partner + ' noch ' + str('%.2f' % self_diff) + '€.'
    ergebnis += ergebnis_satz

    result_context.add('str_ergebnis', ergebnis.replace('<br>', '\n'))
    result_context.add('ausgabe_partner', "%.2f" % abs(ausgabe_partner))
    result_context.add('ausgabe_self', "%.2f" % abs(ausgabe_self))
    result_context.add('self_diff', "%.2f" % self_diff)
    result_context.add('partner_diff', "%.2f" % partner_diff)
    result_context.add('self_soll', "%.2f" % abs(self_soll))
    result_context.add('partner_soll', "%.2f" % abs(partner_soll))
    result_context.add('ausgabe_gesamt', "%.2f" % abs(ausgabe_gesamt))
    result_context.add('ergebnis', ergebnis)
    result_context.add('myname', name_self)
    result_context.add('partnername', name_partner)

    result_context.add('mindate', convert_date_if_present(datum_to_german, mindate))
    result_context.add('maxdate', convert_date_if_present(datum_to_german, maxdate))
    result_context.add('count', context.gemeinsamebuchungen().select().count())

    result_context.add('set_mindate_rfc', convert_date_if_present(datum_to_string, set_mindate))
    result_context.add('set_maxdate_rfc', convert_date_if_present(datum_to_string, set_maxdate))
    result_context.add('set_mindate', convert_date_if_present(datum_to_german, set_mindate))
    result_context.add('set_maxdate', convert_date_if_present(datum_to_german, set_maxdate))
    result_context.add('set_count', selector.count())
    result_context.add('set_verhaeltnis_real', int(set_verhaeltnis))

    result_context.add('kategorien',
                       context.einzelbuchungen().get_alle_kategorien(hide_ausgeschlossene_kategorien=True))

    return result_context


def convert_date_if_present(converter_func, value):
    if not isinstance(value, datetime.date):
        return ''
    return converter_func(value)


def replay_value_if_defined(context: PageContext, replay_name, request: Request, default: bool | object | int = False):
    if request.is_post_parameter_set(replay_name):
        context.add(replay_name, request.values[replay_name])
    elif default:
        context.add(replay_name, default)


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='gemeinsame_buchungen/gemeinsamabrechnen.html',
        context_creator=lambda db: AbrechnenVorschauContext(
            name=db.name,
            einzelbuchungen=db.einzelbuchungen,
            gemeinsamebuchungen=db.gemeinsamebuchungen,
            configuration=configuration_provider.CONFIGURATION_PROVIDER
        )
    )
