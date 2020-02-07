import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth/auth.service';
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
    this.menu = this.menuItemService.getAllDesktopElements();
  }

  logout(){
    this.authService.logout();
  }

  navigateTo(url: string, drawer){
    drawer.close();
    this.router.navigate([url]);
  }

  open(menuItem) {
    menuItem.opened = true;
  }

  close(menuItem) {
    menuItem.opened = false;
  }

}
