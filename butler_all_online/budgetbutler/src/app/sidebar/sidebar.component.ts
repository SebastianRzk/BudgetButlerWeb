import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { Router } from '@angular/router';
import { routerNgProbeToken } from '@angular/router/src/router_module';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {

  constructor(private authService: AuthService, private router: Router) { }

  menu = [
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
          icon: 'add'
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
          icon: 'add'
        }
      ]
    }
  ];

  ngOnInit() {
  }

  logout(){
    this.authService.logout();
  }

  navigateTo(url: string){
    console.log("Navigating to: " + url);
    this.router.navigate([url]);
  }

  open(menuItem) {
    menuItem.opened = true;
  }

  close(menuItem) {
    menuItem.opened = false;
  }
}
