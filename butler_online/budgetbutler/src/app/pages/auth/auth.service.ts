import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {ApiProviderService} from '../../domain/api-provider.service';
import {NotificationService} from '../../domain/notification.service';
import {ERROR_LOGIN_RESULT} from '../../domain/model';
import {BehaviorSubject, Observable} from 'rxjs';
import {LOGIN_OFFLINE_ROUTE, LOGIN_ROUTE} from '../../app-routes';
import {LocalStorageService} from '../../local-storage.service';
import { map } from "rxjs/operators";


@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private auth: BehaviorSubject<UserSession> = new BehaviorSubject<UserSession>(LOGGED_OUT);
  public readonly auth$: Observable<UserSession> = this.auth.asObservable();
  public readonly loggedIn$: Observable<boolean> = this.auth$.pipe(map(auth => auth.loggedIn));

  private httpClient: HttpClient = inject(HttpClient);
  private router: Router = inject(Router);
  private api: ApiProviderService = inject(ApiProviderService);
  private notificationService: NotificationService = inject(NotificationService);
  private localStorageService: LocalStorageService = inject(LocalStorageService);

  checkLoginState(localLogin?: LocalLoginConfiguration) {
    this.httpClient.get<UserSession | null>(this.api.getUrl('login/user')).subscribe(
      data => {
        if (data != null && data.loggedIn) {
          if (this.localStorageService.isOfflineLogin() || localLogin) {
            this.router.navigate([LOGIN_OFFLINE_ROUTE]);
          }
          this.auth.next(
            {
              userName: data.userName,
              loggedIn: true
            }
          );
        } else {
          if (localLogin) {
            this.localStorageService.setOfflineLogin(localLogin.redirect);
          }
          this.handleLogOut();
        }
      },
      error => {
        this.notificationService.handleError(error, ERROR_LOGIN_RESULT, 'Login fehlgeschlagen');
        this.handleLogOut();
      }
    );
  }

  callLogout(): Observable<LogoutState> {
    return this.httpClient.post<LogoutState>(this.api.getUrl("login/logout"), {});
  }


  handleLogOut() {
    this.auth.next(LOGGED_OUT);
    this.router.navigate([LOGIN_ROUTE]);
  }
}

export interface UserSession {
  userName: string;
  loggedIn: boolean;
}

export const LOGGED_OUT: UserSession = {
  userName: '',
  loggedIn: false,
};

export interface LogoutState {
  logoutUrl?: string,
}

export interface LocalLoginConfiguration {
  redirect: string;
}
