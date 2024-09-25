import { Component, inject, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { MenuItemService } from '../../domain/menu-item.service';
import { BehaviorSubject, Observable } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { MatButton } from '@angular/material/button';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';

@Component({
    selector: 'app-offline-login',
    templateUrl: './offline-login.component.html',
    styleUrls: ['./offline-login.component.css'],
    standalone: true,
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatButton, AsyncPipe]
})
export class OfflineLoginComponent implements OnInit {

  private authService: AuthService = inject(AuthService);
  private menuitemService: MenuItemService = inject(MenuItemService);


  private disabledSubject = new BehaviorSubject(false);

  disabled$: Observable<boolean> = this.disabledSubject.asObservable();


  ngOnInit() {
    this.menuitemService.close();
    this.authService.checkLoginState(true);
    this.authService.auth$.subscribe(
      element => this.disabledSubject.next(!element.loggedIn)
    );
  }

  navigate() {
    window.location.href = 'api/login/offline/access';
  }
}

