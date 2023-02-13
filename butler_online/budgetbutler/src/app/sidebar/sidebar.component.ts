import {BreakpointObserver} from '@angular/cdk/layout';
import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthContainer, AuthService} from '../auth/auth.service';
import {MenuitemService} from '../menuitem.service';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  menu = [];
  opened = true;
  isSmallScreen = this.breakpointObserver.isMatched('(max-width: 799px)');
  user$: Observable<AuthContainer>;

  constructor(public authService: AuthService,
              private router: Router,
              private menuItemService: MenuitemService,
              private breakpointObserver: BreakpointObserver) {

    this.user$ = authService.auth$;
  }

  ngOnInit() {
    this.menu = this.menuItemService.getAllDesktopElements();

    if (this.isSmallScreen) {
      this.opened = false;
    }
  }

  logout() {
    this.authService.logout();
  }

  navigateTo(url: string, drawer) {
    if (this.isSmallScreen) {
      drawer.close();
    }
    this.router.navigate([url]);
  }

}
