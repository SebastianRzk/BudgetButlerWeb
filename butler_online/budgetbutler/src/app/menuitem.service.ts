import {Injectable} from '@angular/core';
import {ADD_SCHNELLEINSTIEG_ROUTE, ALLE_EINZELBUCHUNGEN_ROUTE, ALLE_GEMEINSAME_BUCHUNGEN_ROUTE, SETTINGS_ROUTE} from './app-routes';
import {BehaviorSubject} from 'rxjs';


export class MenuItem {
  title: string;
  url: string;
  icon: string;
}

const SCHNELLEINSTIEG = {
  title: 'Buchung erfassen',
  url: ADD_SCHNELLEINSTIEG_ROUTE,
  icon: 'add_circle_outline'
};

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

const EINSTELLUNGEN = {
  title: 'Einstellungen',
  url: SETTINGS_ROUTE,
  icon: 'settings'
};

export const MENU_ITEMS: MenuItem[] = [
  SCHNELLEINSTIEG,
  ALLE_EINZELBUCHUNGEN,
  ALLE_GEMEINSAME_BUCHUNGEN,
  EINSTELLUNGEN
];


@Injectable({
  providedIn: 'root'
})
export class MenuitemService {

  private opened = new BehaviorSubject(false);

  public readonly opened$ = this.opened.asObservable();

  constructor() {
  }

  public open() {
    this.opened.next(true);
  }

  public close() {
    this.opened.next(false);
  }


}
