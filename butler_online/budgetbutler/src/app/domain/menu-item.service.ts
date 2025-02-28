import { Injectable } from '@angular/core';
import {
  ADD_DAUERAUFTRAG_ROUTE,
  ADD_SCHNELLEINSTIEG_ROUTE,
  ALLE_EINZELBUCHUNGEN_ROUTE,
  ALLE_GEMEINSAME_BUCHUNGEN_ROUTE,
  DAUERAUFTRAEGE_ROUTE,
  GEMEINSAME_BUCHUNGEN_UEBERSICHT_ROUTE,
  GEMEINSAME_DAUERAUFTRAEGE_ROUTE,
  KATEGORIEN_ROUTE,
  PERSOENLICHE_BUCHUNGEN_UEBERSICHT_ROUTE,
  SETTINGS_ROUTE,
} from '../app-routes';
import { BehaviorSubject } from 'rxjs';
import { map } from "rxjs/operators";

export interface MenuItem {
  title: string;
  url: string;
  icon: string;
}

const SCHNELLEINSTIEG: MenuItem = {
  title: 'Buchung erfassen',
  url: ADD_SCHNELLEINSTIEG_ROUTE,
  icon: 'add_circle_outline'
};

const ADD_DAUERAUFTRAG: MenuItem = {
  title: 'Dauerauftrag erfassen',
  url: ADD_DAUERAUFTRAG_ROUTE,
  icon: 'add_circle_outline'
}
const DAUERAUFTRAEGE: MenuItem = {
  title: 'Dauerauftraege',
  url: DAUERAUFTRAEGE_ROUTE,
  icon: 'timer'
}
const GEMEINSAME_DAUERAUFTRAEGE: MenuItem = {
  title: 'Gemeinsame Dauerauftraege',
  url: GEMEINSAME_DAUERAUFTRAEGE_ROUTE,
  icon: 'timer'
}

const ALLE_EINZELBUCHUNGEN: MenuItem = {
  title: 'Persönliche Buchungen',
  url: ALLE_EINZELBUCHUNGEN_ROUTE,
  icon: 'format_list_bulleted'
};

const UEBERSICHT_PERSOENLICHE_BUCHUNGEN: MenuItem = {
  title: 'Pers. Buchungen Übersicht',
  url: PERSOENLICHE_BUCHUNGEN_UEBERSICHT_ROUTE,
  icon: 'donut_small'
};

const ALLE_GEMEINSAME_BUCHUNGEN: MenuItem = {
  title: 'Gemeinsame Buchungen',
  url: ALLE_GEMEINSAME_BUCHUNGEN_ROUTE,
  icon: 'format_list_bulleted'
};

const UEBERSICHT_GEMEINSAME_BUCHUNGEN: MenuItem = {
  title: 'Gem. Buchungen Übersicht',
  url: GEMEINSAME_BUCHUNGEN_UEBERSICHT_ROUTE,
  icon: 'donut_small'
};

const KATEGORIEN: MenuItem = {
  title: 'Kategorien verwalten',
  url: KATEGORIEN_ROUTE,
  icon: 'category'
};

const EINSTELLUNGEN: MenuItem = {
  title: 'Einstellungen',
  url: SETTINGS_ROUTE,
  icon: 'settings'
};

export const MENU_ITEMS: MenuItem[] = [
  SCHNELLEINSTIEG,
  ADD_DAUERAUFTRAG,
  ALLE_EINZELBUCHUNGEN,
  UEBERSICHT_PERSOENLICHE_BUCHUNGEN,
  ALLE_GEMEINSAME_BUCHUNGEN,
  UEBERSICHT_GEMEINSAME_BUCHUNGEN,
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

  public readonly closed$ = this.opened$.pipe(map(opened => !opened));

  public open() {
    this.opened.next(true);
  }

  public close() {
    this.opened.next(false);
  }


}
