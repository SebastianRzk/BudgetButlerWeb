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

@Injectable({
  providedIn: 'root'
})
export class MenuitemService {

  constructor() { }

  get(): MenuItem[] {
    return [
      {
        title: 'Dashboard',
        type: 'link',
        url: DASHBOARD_ROUTE,
        icon: 'bar_chart'
      },
      {
        title: 'Schnellerfassung',
        type: 'link',
        url: ADD_SCHNELLEINSTIEG_ROUTE,
        icon: 'add_circle_outline'
      },
      {
        title: 'Einzelbuchungen',
        type: 'node',
        opened: false,
        children: [
          {
            title: 'Neue Ausgabe',
            type: 'link',
            url: ADD_AUSGABE_ROUTE,
            icon: 'add_circle_outline'
          },
          {
            title: 'Neue Einnahme',
            type: 'link',
            url: ADD_EINNAHME_ROUTE,
            icon: 'add_circle_outline'
          },
          {
            title: 'Alle Buchungen',
            type: 'link',
            url: ALLE_EINZELBUCHUNGEN_ROUTE,
            icon: 'format_list_bulleted'
          }
        ]
      },
      {
        title: 'Gemeinsame Buchungen',
        type: 'node',
        opened: false,
        children: [
          {
            title: 'Neue gemeinsame Ausgabe',
            type: 'link',
            url: ADD_GEMEINSAME_BUCHUNG_ROUTE,
            icon: 'add_circle_outline'
          },
          {
            title: 'Alle gemeinsame Buchungen',
            type: 'link',
            url: ALLE_GEMEINSAME_BUCHUNGEN_ROUTE,
            icon: 'format_list_bulleted'
          }
        ]
      },
      {
        title: 'Einstellungen',
        type: 'link',
        url: SETTINGS_ROUTE,
        icon: 'settings'
      }

    ];
  }

  getFlat() {
    const elements = [];
    this.get().forEach(
      item => {
        if (item.type === 'link') {
          elements.push(item);
        } else {
          item.children.forEach(
            child => {
              elements.push({ ...child });
            }
          );
        }
      }
    );
    return elements;
  }
}
