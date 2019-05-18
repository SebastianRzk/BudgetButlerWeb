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
            url: 'addgemeinsam',
            icon: 'add_box'
          }
        ]
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
