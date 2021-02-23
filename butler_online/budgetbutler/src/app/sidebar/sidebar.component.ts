import { BreakpointObserver } from '@angular/cdk/layout';
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

  constructor(public authService: AuthService,
              private router: Router,
              private menuItemService: MenuitemService,
              private breakpointObserver: BreakpointObserver) { }

  menu = [];
  opened = true;

  isSmallScreen = this.breakpointObserver.isMatched('(max-width: 799px)');

  ngOnInit() {
    this.menu = this.menuItemService.getAllDesktopElements();

    if (this.isSmallScreen){
      this.opened = false;
    }
  }

  logout(){
    this.authService.logout();
  }

  navigateTo(url: string, drawer){
    if (this.isSmallScreen){
      drawer.close();
    }
    this.router.navigate([url]);
  }

}
