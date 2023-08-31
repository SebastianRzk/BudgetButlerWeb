from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.dauerauftraege import Dauerauftraege
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_redirect_page_context
from butler_offline.viewcore import routes
from butler_offline.views.core.configuration.language import RENAME_SUCCESSFULL


class RenameContext:
    def __init__(self,
                 einzelbuchungen: Einzelbuchungen,
                 dauerauftraege: Dauerauftraege):
        self._einzelbuchungen = einzelbuchungen
        self._dauerauftraege = dauerauftraege

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen

    def dauerauftraege(self) -> Dauerauftraege:
        return self._dauerauftraege


def handle_request(request, context: RenameContext):
    alter_kategorie_name = str(request.values['kategorie_alt'])
    neuer_kategorie_name = str(request.values['kategorie_neu'])

    anzahl_betroffener_einzelbuchungen = (context.einzelbuchungen()
                                          .select()
                                          .select_kategorie(kategorie=alter_kategorie_name)
                                          .select_statischen_content()
                                          .count())
    anzahl_betroffener_dauerauftraege = (context.dauerauftraege()
                                         .select()
                                         .select_kategorie(kategorie=alter_kategorie_name)
                                         .count())

    context.einzelbuchungen().rename_kategorie(
        alter_name=alter_kategorie_name,
        neuer_name=neuer_kategorie_name
    )
    context.dauerauftraege().rename_kategorie(
        alter_name=alter_kategorie_name,
        neuer_name=neuer_kategorie_name
    )

    return generate_redirect_page_context(
        redirect_target_url='{}?{}={}'.format(routes.CORE_CONFIGURATION,
                                              routes.CORE_CONFIGURATION_PARAM_SUCCESS_MESSAGE,
                                              RENAME_SUCCESSFULL.format(
                                                  alter_kategorie_name,
                                                  neuer_kategorie_name,
                                                  anzahl_betroffener_einzelbuchungen,
                                                  anzahl_betroffener_dauerauftraege
                                              )))


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: RenameContext(
            einzelbuchungen=db.einzelbuchungen,
            dauerauftraege=db.dauerauftraege
        ),
        html_base_page='core/configuration.html'
    )
