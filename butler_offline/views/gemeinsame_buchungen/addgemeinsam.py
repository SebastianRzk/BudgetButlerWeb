from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import from_double_to_german, datum, datum_to_string, datum_to_german
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.context.builder import generate_transactional_page_context
from butler_offline.viewcore.template import fa
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from typing import List
import logging
from butler_offline.viewcore.http import Request


class AddGemeinsameBuchungContext:
    def __init__(self,
                 gemeinsame_buchungen: Gemeinsamebuchungen,
                 partner_name: str,
                 database_name: str,
                 kategorien: List[str]):
        self._gemeinsame_buchungen = gemeinsame_buchungen
        self._partner_name = partner_name
        self._database_name = database_name
        self._kategorien = kategorien

    def gemeinsame_buchungen(self) -> Gemeinsamebuchungen:
        return self._gemeinsame_buchungen

    def partner_name(self) -> str:
        return self._partner_name

    def kategorien(self) -> List[str]:
        return self._kategorien

    def database_name(self) -> str:
        return self._database_name


def handle_request(request: Request, context: AddGemeinsameBuchungContext):
    if request.post_action_is('add'):
        date = datum(request.values['date'])
        value = request.values['wert'].replace(",", ".")
        value = float(value)
        value = value * -1
        if "edit_index" in request.values:
            context.gemeinsame_buchungen().edit(int(request.values['edit_index']),
                                                datum=date,
                                                name=str(request.values['name']),
                                                kategorie=request.values['kategorie'],
                                                wert=value,
                                                person=request.values['person']
                                                )
            non_persisted_state.add_changed_gemeinsamebuchungen(
                {
                    'fa': fa.pencil,
                    'datum': datum_to_german(date),
                    'kategorie': request.values['kategorie'],
                    'name': request.values['name'],
                    'wert': from_double_to_german(value),
                    'person': request.values['person']
                })

        else:
            context.gemeinsame_buchungen().add(ausgaben_datum=date,
                                               kategorie=request.values['kategorie'],
                                               ausgaben_name=request.values['name'],
                                               wert="%.2f" % value,
                                               person=request.values['person'])
            non_persisted_state.add_changed_gemeinsamebuchungen(
                {
                    'fa': fa.plus,
                    'datum': datum_to_german(date),
                    'kategorie': request.values['kategorie'],
                    'name': request.values['name'],
                    'wert': from_double_to_german(value),
                    'person': request.values['person']
                })

    result_context = generate_transactional_page_context("addgemeinsam")
    result_context.add('approve_title', 'Gemeinsame Ausgabe hinzufügen')
    if request.post_action_is('edit'):
        logging.info('Please edit: %s', request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = context.gemeinsame_buchungen().get(db_index)
        default_item = {
            'edit_index': str(db_index),
            'datum': datum_to_string(db_row['Datum']),
            'name': db_row['Name'],
            'wert': from_double_to_german(db_row['Wert'] * -1),
            'kategorie': db_row['Kategorie'],
            'person': db_row['Person']
        }

        result_context.add('default_item', default_item)
        result_context.add('bearbeitungsmodus', True)
        result_context.add('edit_index', db_index)
        result_context.add('approve_title', 'Gemeinsame Ausgabe aktualisieren')

    if not result_context.contains('default_item'):
        result_context.add('default_item', {
            'name': '',
            'wert': '',
            'datum': ''
        })

    result_context.add('personen', [context.database_name(), context.partner_name()])
    result_context.add('kategorien', sorted(context.kategorien()))
    result_context.add('letzte_erfassung', reversed(non_persisted_state.get_changed_gemeinsamebuchungen()))
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='gemeinsame_buchungen/addgemeinsam.html',
        context_creator=lambda db: AddGemeinsameBuchungContext(
            gemeinsame_buchungen=db.gemeinsamebuchungen,
            database_name=db.name,
            kategorien=db.einzelbuchungen.get_kategorien_ausgaben(hide_ausgeschlossene_kategorien=True),
            partner_name=viewcore.name_of_partner()
        )
    )
