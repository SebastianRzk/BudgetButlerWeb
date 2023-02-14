import {Component, OnInit} from '@angular/core';
import {MENU_ITEMS, MenuitemService} from '../../menuitem.service';
import {Observable} from 'rxjs';
import {MatDrawerMode} from '@angular/material/sidenav';
import {AuthContainer, AuthService} from '../../auth/auth.service';
import {Router} from '@angular/router';
import {BreakpointObserver} from '@angular/cdk/layout';
import {map} from 'rxjs/operators';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  menu = MENU_ITEMS;

  opened$: Observable<boolean>;
  closed$: Observable<boolean>;
  mode: MatDrawerMode = 'side';
  isSmallScreen = this.breakpointObserver.isMatched('(max-width: 799px)');
  user$: Observable<AuthContainer>;

  constructor(public authService: AuthService,
              private router: Router,
              public menuService: MenuitemService,
              private breakpointObserver: BreakpointObserver) {

    this.user$ = authService.auth$;
    this.opened$ = menuService.opened$;
    this.closed$ = this.opened$.pipe(map(opened => !opened));
  }

  ngOnInit() {
    if (this.isSmallScreen) {
      this.mode = 'over';
      this.menuService.close();
    } else {
      this.menuService.open();
    }
  }

  logout() {
    this.authService.logout();
  }

  navigateTo(url: string) {
    if (this.isSmallScreen) {
      this.menuService.close();
    }
    this.router.navigate([url]);
  }
}
