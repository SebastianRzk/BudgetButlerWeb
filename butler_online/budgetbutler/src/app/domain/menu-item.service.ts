import {Injectable} from '@angular/core';
import {
  ADD_DAUERAUFTRAG_ROUTE,
  ADD_SCHNELLEINSTIEG_ROUTE,
  ALLE_EINZELBUCHUNGEN_ROUTE,
  ALLE_GEMEINSAME_BUCHUNGEN_ROUTE, DAUERAUFTRAEGE_ROUTE, GEMEINSAME_DAUERAUFTRAEGE_ROUTE, KATEGORIEN_ROUTE,
  SETTINGS_ROUTE
} from '../app-routes';
import {BehaviorSubject} from 'rxjs';


export interface MenuItem {
  title: string;
  url: string;
  icon: string;
}

const SCHNELLEINSTIEG = {
  title: 'Buchung erfassen',
  url: ADD_SCHNELLEINSTIEG_ROUTE,
  icon: 'add_circle_outline'
};

const ADD_DAUERAUFTRAG = {
  title: 'Dauerauftrag erfassen',
  url: ADD_DAUERAUFTRAG_ROUTE,
  icon: 'add_circle_outline'
}
const DAUERAUFTRAEGE = {
  title: 'Dauerauftraege',
  url: DAUERAUFTRAEGE_ROUTE,
  icon: 'timer'
}
const GEMEINSAME_DAUERAUFTRAEGE = {
  title: 'Gemeinsame Dauerauftraege',
  url: GEMEINSAME_DAUERAUFTRAEGE_ROUTE,
  icon: 'timer'
}

const ALLE_EINZELBUCHUNGEN = {
  title: 'Persönliche Buchungen',
  url: ALLE_EINZELBUCHUNGEN_ROUTE,
  icon: 'format_list_bulleted'
};

const ALLE_GEMEINSAME_BUCHUNGEN = {
  title: 'Gemeinsame Buchungen',
  url: ALLE_GEMEINSAME_BUCHUNGEN_ROUTE,
  icon: 'format_list_bulleted'
};

const KATEGORIEN = {
  title: 'Kategorien verwalten',
  url: KATEGORIEN_ROUTE,
  icon: 'category'
};

const EINSTELLUNGEN = {
  title: 'Einstellungen',
  url: SETTINGS_ROUTE,
  icon: 'settings'
};

export const MENU_ITEMS: MenuItem[] = [
  SCHNELLEINSTIEG,
  ADD_DAUERAUFTRAG,
  ALLE_EINZELBUCHUNGEN,
  ALLE_GEMEINSAME_BUCHUNGEN,
  DAUERAUFTRAEGE,
  GEMEINSAME_DAUERAUFTRAEGE,
  KATEGORIEN,
  EINSTELLUNGEN
];


@Injectable({
  providedIn: 'root'
})
export class MenuItemService {

  private opened = new BehaviorSubject(false);

  public readonly opened$ = this.opened.asObservable();

  public open() {
    this.opened.next(true);
  }

  public close() {
    this.opened.next(false);
  }


}
