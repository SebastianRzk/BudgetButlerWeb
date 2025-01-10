import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {ApiProviderService} from '../../domain/api-provider.service';
import {NotificationService} from '../../domain/notification.service';
import {ERROR_LOGIN_RESULT} from '../../domain/model';
import {BehaviorSubject, Observable} from 'rxjs';
import {ADD_SCHNELLEINSTIEG_ROUTE, LOGIN_OFFLINE_ROUTE, LOGIN_ROUTE} from '../../app-routes';
import {LocalStorageService} from '../../local-storage.service';


@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private auth: BehaviorSubject<AuthContainer> = new BehaviorSubject<AuthContainer>(LOGGED_OUT);
  public readonly auth$: Observable<AuthContainer> = this.auth.asObservable();

  private httpClient: HttpClient = inject(HttpClient);
  private router: Router = inject(Router);
  private api: ApiProviderService = inject(ApiProviderService);
  private notificationService: NotificationService = inject(NotificationService);
  private localStorageService: LocalStorageService = inject(LocalStorageService);

  login(username: string, password: string) {
    const body = new FormData();
    body.append('email', username);
    body.append('password', password);

    this.httpClient.post<AuthContainer>(this.api.getUrl('login/user'), body).subscribe(
      data => {
        if (data != null && data.userName) {
          this.auth.next(
            {
              userName: data.userName,
              loggedIn: true
            }
          );

          this.router.navigate([ADD_SCHNELLEINSTIEG_ROUTE]);
        } else {
          this.auth.next(LOGGED_OUT);
          this.notificationService.log(ERROR_LOGIN_RESULT, 'Login');
        }
      },
      error => {
        this.notificationService.handleError(error, ERROR_LOGIN_RESULT, 'Login fehlgeschlagen');
        this.auth.next(LOGGED_OUT);
      }
    );
  }

  checkLoginState(localLogin?: LocalLoginConfiguration) {
    this.httpClient.get<AuthContainer | null>(this.api.getUrl('login/user')).subscribe(
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

export interface AuthContainer {
  userName: string;
  loggedIn: boolean;
}

export const LOGGED_OUT: AuthContainer = {
  userName: '',
  loggedIn: false,
};

export interface LogoutState {
  id_token: string,
  logoutUrl?: string,
}

export interface LocalLoginConfiguration {
  redirect: string;
}
