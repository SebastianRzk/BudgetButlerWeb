import {Component, inject, OnInit} from '@angular/core';
import {AuthService} from '../auth/auth.service';
import {MenuItemService} from '../../domain/menu-item.service';
import {BehaviorSubject, firstValueFrom, Observable, Subject} from 'rxjs';
import {AsyncPipe, NgOptimizedImage} from '@angular/common';
import {MatButton} from '@angular/material/button';
import {MatCard, MatCardHeader, MatCardTitle, MatCardContent} from '@angular/material/card';
import {LocalStorageService} from "../../local-storage.service";
import {map} from "rxjs/operators";
import {MatDivider} from "@angular/material/divider";

@Component({
    selector: 'app-offline-login',
    templateUrl: './offline-login.component.html',
    styleUrls: ['./offline-login.component.css'],
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatButton, AsyncPipe, NgOptimizedImage, MatDivider]
})
export class OfflineLoginComponent implements OnInit {

  private authService: AuthService = inject(AuthService);
  private menuitemService: MenuItemService = inject(MenuItemService);

  private disabledSubject = new BehaviorSubject(false);
  private localStoreService: LocalStorageService = inject(LocalStorageService);

  disabled$: Observable<boolean> = this.disabledSubject.asObservable();

  private localLoginUrl: Subject<string> = new BehaviorSubject('');

  visibleLocalLoginUrl$: Observable<string> = this.localLoginUrl.asObservable().pipe(map(url => {
    if (url === DEFAULT_REDIRECT) {
      return '';
    }
    return url;
  }));

  ngOnInit() {
    this.menuitemService.close();

    const redirectLocation = this.getRedirect();
    this.localLoginUrl.next(redirectLocation);

    this.authService.checkLoginState({
      redirect: redirectLocation
    });
    this.authService.auth$.subscribe(
      element => this.disabledSubject.next(!element.loggedIn)
    );
  }

  navigate() {
    this.localStoreService.removeLocalLogin();
    firstValueFrom(this.localLoginUrl).then(url => {
      window.location.href = 'api/login/offline/access?redirect=' + url;
    })
  }
  ablehnen() {
    this.localStoreService.removeLocalLogin();
    firstValueFrom(this.localLoginUrl).then(url => {
      window.location.href = url;
    })
  }


  getRedirect(): string {
    const queryParam: string | null =  new URLSearchParams(window.location.search).get('redirect');
    console.log('redirect to from query param ' + queryParam);
    if (queryParam) {
      return queryParam.toString();
    }
    const localStorageUrl: string | null = this.localStoreService.getLocalLoginUrl();

    console.log('redirect to from local storage ' + localStorageUrl);
    if (localStorageUrl) {
      return localStorageUrl;
    }
    return DEFAULT_REDIRECT;
  }
}


const DEFAULT_REDIRECT = 'http://localhost:5000';
