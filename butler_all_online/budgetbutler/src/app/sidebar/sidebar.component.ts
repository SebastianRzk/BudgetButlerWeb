import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { Router } from '@angular/router';
import { routerNgProbeToken } from '@angular/router/src/router_module';
import { MenuitemService } from '../menuitem.service';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {

  constructor(public authService: AuthService, private router: Router, private menuItemService: MenuitemService) { }

  menu = []

  ngOnInit() {
    this.menu = this.menuItemService.get();
  }

  logout(){
    this.authService.logout();
  }

  navigateTo(url: string){
    this.router.navigate([url]);
  }

  open(menuItem) {
    menuItem.opened = true;
  }

  close(menuItem) {
    menuItem.opened = false;
  }
}
