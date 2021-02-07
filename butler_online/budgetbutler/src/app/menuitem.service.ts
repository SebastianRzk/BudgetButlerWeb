import { Injectable } from '@angular/core';
import { ADD_SCHNELLEINSTIEG_ROUTE, ALLE_EINZELBUCHUNGEN_ROUTE, ALLE_GEMEINSAME_BUCHUNGEN_ROUTE, SETTINGS_ROUTE } from './app-routes';


export class MenuItem {
  title: string;
  type: string;
  url?: string;
  icon?: string;
  opened?: boolean;
  children?: MenuItem[];
}

const SCHNELLEINSTIEG = {
  title: 'Buchung erfassen',
  type: 'link',
  url: ADD_SCHNELLEINSTIEG_ROUTE,
  icon: 'add_circle_outline'
};

const ALLE_EINZELBUCHUNGEN = {
  title: 'Persönliche Buchungen',
  type: 'link',
  url: ALLE_EINZELBUCHUNGEN_ROUTE,
  icon: 'format_list_bulleted'
};

const ALLE_GEMEINSAME_BUCHUNGEN = {
  title: 'Gemeinsame Buchungen',
  type: 'link',
  url: ALLE_GEMEINSAME_BUCHUNGEN_ROUTE,
  icon: 'format_list_bulleted'
};

const EINSTELLUNGEN = {
  title: 'Einstellungen',
  type: 'link',
  url: SETTINGS_ROUTE,
  icon: 'settings'
};


@Injectable({
  providedIn: 'root'
})
export class MenuitemService {

  constructor() { }

  getAllDesktopElements(): MenuItem[] {
    return [
      SCHNELLEINSTIEG,
      ALLE_EINZELBUCHUNGEN,
      ALLE_GEMEINSAME_BUCHUNGEN,
      EINSTELLUNGEN
    ];
  }
}
