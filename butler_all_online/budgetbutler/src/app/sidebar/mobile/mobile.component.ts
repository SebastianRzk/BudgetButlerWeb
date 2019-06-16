import { Component, OnInit } from '@angular/core';
import { MenuitemService } from '../../menuitem.service';
import { Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-mobile-sidebar',
  templateUrl: './mobile.component.html',
  styleUrls: ['./mobile.component.css']
})
export class MobileComponent implements OnInit {

  public menuOpened = false;
  public menu = [];

  constructor(private menuitemService: MenuitemService, private router: Router, private authService: AuthService) { }

  ngOnInit() {
    this.menu = this.menuitemService.getMainMobileMenuElements();
  }

  toggleMenu() {
    this.menuOpened = !this.menuOpened;
  }

  navigateTo(url: string){
    this.menuOpened = false;
    this.router.navigate([url]);
  }

  logout(){
    this.authService.logout();
  }

}
