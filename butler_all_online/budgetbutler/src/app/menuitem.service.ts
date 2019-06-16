import { Injectable } from '@angular/core';
import { DASHBOARD_ROUTE, ADD_SCHNELLEINSTIEG_ROUTE, ADD_AUSGABE_ROUTE, ADD_EINNAHME_ROUTE, ALLE_EINZELBUCHUNGEN_ROUTE, ADD_GEMEINSAME_BUCHUNG_ROUTE, ALLE_GEMEINSAME_BUCHUNGEN_ROUTE, SETTINGS_ROUTE } from './app-routes';


export class MenuItem {
  title: string;
  type: string;
  url?: string;
  icon?: string;
  opened?: boolean;
  children?: MenuItem[];
}

const DASHBOARD = {
  title: 'Dashboard',
  type: 'link',
  url: DASHBOARD_ROUTE,
  icon: 'bar_chart'
};

const SCHNELLEINSTIEG = {
  title: 'Schnellerfassung',
  type: 'link',
  url: ADD_SCHNELLEINSTIEG_ROUTE,
  icon: 'add_circle_outline'
};

const NEUE_AUSGABE = {
  title: 'Neue Ausgabe',
  type: 'link',
  url: ADD_AUSGABE_ROUTE,
  icon: 'add_circle_outline'
};

const NEUE_EINNAHME = {
  title: 'Neue Einnahme',
  type: 'link',
  url: ADD_EINNAHME_ROUTE,
  icon: 'add_circle_outline'
};

const ALLE_EINZELBUCHUNGEN = {
  title: 'Übersicht persönliche Buchungen',
  type: 'link',
  url: ALLE_EINZELBUCHUNGEN_ROUTE,
  icon: 'format_list_bulleted'
};

const NEUE_GEMEINSAME_BUCHUNG = {
  title: 'Neue gemeinsame Ausgabe',
  type: 'link',
  url: ADD_GEMEINSAME_BUCHUNG_ROUTE,
  icon: 'add_circle_outline'
};

const ALLE_GEMEINSAME_BUCHUNGEN = {
  title: 'Übersicht gemeinsame Buchungen',
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
      DASHBOARD,
      SCHNELLEINSTIEG,
      {
        title: 'Einzelbuchungen',
        type: 'node',
        opened: false,
        children: [
          NEUE_AUSGABE,
          NEUE_EINNAHME,
          ALLE_EINZELBUCHUNGEN
        ]
      },
      {
        title: 'Gemeinsame Buchungen',
        type: 'node',
        opened: false,
        children: [
          NEUE_GEMEINSAME_BUCHUNG,
          ALLE_GEMEINSAME_BUCHUNGEN
        ]
      },
      EINSTELLUNGEN
    ];
  }

  getMainMobileMenuElements() {
    return [
      SCHNELLEINSTIEG,
      ALLE_EINZELBUCHUNGEN,
      ALLE_GEMEINSAME_BUCHUNGEN,
    ];
  }


  getAdditionalMobileMenuElements() {
    return [
      DASHBOARD,
      NEUE_EINNAHME,
      NEUE_AUSGABE,
      NEUE_GEMEINSAME_BUCHUNG,
      EINSTELLUNGEN
    ];
  }
}
