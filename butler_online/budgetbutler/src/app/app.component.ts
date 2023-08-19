import {Component, OnInit} from '@angular/core';
import {MenuitemService} from './domain/menuitem.service';
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
  mode: MatDrawerMode = 'side';
  isSmallScreen = this.breakpointObserver.isMatched('(max-width: 799px)');

  user$: Observable<AuthContainer>;

  opened$: Observable<boolean>;

  constructor(
    public menuService: MenuitemService,
    private breakpointObserver: BreakpointObserver,
    authService: AuthService) {
    this.user$ = authService.auth$;
    this.opened$ = menuService.opened$;
  }

  ngOnInit() {
    if (this.isSmallScreen) {
      this.mode = 'over';
      this.menuService.close();
    } else {
      this.menuService.open();
    }
  }

}
