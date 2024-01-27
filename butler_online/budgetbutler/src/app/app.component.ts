import { Component, inject, OnInit } from '@angular/core';
import {MenuItemService} from './domain/menu-item.service';
import {BreakpointObserver} from '@angular/cdk/layout';
import {MatDrawerMode} from '@angular/material/sidenav';
import {AuthContainer, AuthService} from './pages/auth/auth.service';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  private authService: AuthService = inject(AuthService);
  public menuService: MenuItemService = inject(MenuItemService);
  private breakpointObserver: BreakpointObserver = inject(BreakpointObserver);

  mode: MatDrawerMode = 'side';
  isSmallScreen = this.breakpointObserver.isMatched('(max-width: 799px)');

  user$: Observable<AuthContainer> = this.authService.auth$;

  opened$: Observable<boolean> = this.menuService.opened$;

  ngOnInit() {
    if (this.isSmallScreen) {
      this.mode = 'over';
      this.menuService.close();
    } else {
      this.menuService.open();
    }
  }
}
