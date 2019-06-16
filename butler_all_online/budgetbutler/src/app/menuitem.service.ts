import { Injectable } from '@angular/core';


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
        url: 'dashboard',
        icon: 'bar_chart'
      },
      {
        title: 'Schnellerfassung',
        type: 'link',
        url: 'add',
        icon: 'add_circle_outline'
      },
      {
        title: 'Einzelbuchungen',
        type: 'node',
        opened: true,
        children: [
          {
            title: 'Neue Ausgabe',
            type: 'link',
            url: 'addausgabe',
            icon: 'add_circle_outline'
          },
          {
            title: 'Neue Einnahme',
            type: 'link',
            url: 'addeinnahme',
            icon: 'add_circle_outline'
          },
          {
            title: 'Alle Buchungen',
            type: 'link',
            url: 'allebuchungen',
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
            url: 'addgemeinsameausgabe',
            icon: 'add_circle_outline'
          },
          {
            title: 'Alle gemeinsame Buchungen',
            type: 'link',
            url: 'allegemeinsamebuchungen',
            icon: 'format_list_bulleted'
          }
        ]
      },
      {
        title: 'Einstellungen',
        type: 'link',
        url: 'settings',
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
