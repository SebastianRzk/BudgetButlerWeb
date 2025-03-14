import { Component, inject, OnInit } from '@angular/core';
import { MENU_ITEMS, MenuItemService } from '../../../domain/menu-item.service';
import { Observable } from 'rxjs';
import { MatDrawerMode } from '@angular/material/sidenav';
import { UserSession, AuthService } from '../../auth/auth.service';
import { Router } from '@angular/router';
import { BreakpointObserver } from '@angular/cdk/layout';
import { MatIcon } from '@angular/material/icon';
import { MatButton } from '@angular/material/button';
import { AsyncPipe } from '@angular/common';

@Component({
    selector: 'app-sidebar',
    templateUrl: './sidebar.component.html',
    styleUrls: ['./sidebar.component.css'],
  imports: [MatButton, MatIcon, AsyncPipe]
})
export class SidebarComponent implements OnInit {

  public authService: AuthService = inject(AuthService);
  private router: Router = inject(Router);
  public menuService: MenuItemService = inject(MenuItemService);
  private breakpointObserver: BreakpointObserver = inject(BreakpointObserver);

  menu = MENU_ITEMS;
  mode: MatDrawerMode = 'side';
  isSmallScreen = this.breakpointObserver.isMatched('(max-width: 799px)');
  user$: Observable<UserSession> = this.authService.auth$;

  ngOnInit() {
    if (this.isSmallScreen) {
      this.mode = 'over';
      this.menuService.close();
    } else {
      this.menuService.open();
    }
  }

  logout() {
    this.menuService.close();
    this.router.navigate(['/logout']);
  }

  navigateTo(url: string) {
    if (this.isSmallScreen) {
      this.menuService.close();
    }
    this.router.navigate([url]);
  }
}
