import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {ApiproviderService} from '../../domain/apiprovider.service';
import {NotificationService} from '../../domain/notification.service';
import {ERROR_LOGIN_RESULT, Result} from '../../domain/model';
import {BehaviorSubject, Observable} from 'rxjs';
import {ADD_SCHNELLEINSTIEG_ROUTE} from '../../app-routes';


@Injectable({
  providedIn: 'root',
})
export class AuthService {
  redirectUrl = '';

  private auth = new BehaviorSubject<AuthContainer>(LOGGED_OUT);
  public readonly auth$ = this.auth.asObservable();

  constructor(private httpClient: HttpClient,
              private router: Router,
              private api: ApiproviderService,
              private notificationService: NotificationService) {
  }

  login(username: string, password: string) {
    const body = new FormData();
    body.append('email', username);
    body.append('password', password);

    this.httpClient.post<AuthContainer>(this.api.getUrl('login.php'), body).subscribe(
      data => {
        if (data != null && data.username) {
          this.auth.next(
            {
              username: data.username,
              role: 'user',
              isLoggedIn: true
            }
          );
          this.router.navigate([ADD_SCHNELLEINSTIEG_ROUTE]);
        } else {
          this.auth.next(LOGGED_OUT);
          this.notificationService.log(ERROR_LOGIN_RESULT, 'Login');
        }
      },
      error => {
        this.notificationService.log(ERROR_LOGIN_RESULT, 'Login fehlgeschlagen');
        this.auth.next(LOGGED_OUT);
      }
    );
  }

  checkLoginState() {
    this.httpClient.get<AuthContainer | null>(this.api.getUrl('login.php')).subscribe(
      data => {
        if (data != null && data.username) {
          this.auth.next(
            {
              username: data.username,
              role: 'user',
              isLoggedIn: true
            }
          );
        } else {
          this.handleLogOut();
        }
      },
      error => {
        this.notificationService.log(ERROR_LOGIN_RESULT, 'Login fehlgeschlagen');
        this.handleLogOut();
      }
    );
  }

  public getLogin: () => Observable<AuthContainer> = () => this.httpClient.get<AuthContainer>(this.api.getUrl('login.php'));


  changePassword(oldPassword: string, newPassword: string) {
    const body: ChangePasswordContainer = {
      oldPassword,
      newPassword
    };
    return this.httpClient.post<Result>(this.api.getUrl('changepassword.php'), body).toPromise().then(
      data => {
        this.notificationService.handleServerResult(data, 'Passwort ändern');
      },
      error => {
        this.handleLogOut();
      }
    );
  }


  logout(): void {
    this.httpClient.get<null>(this.api.getUrl('logout.php')).subscribe(() => {
      this.handleLogOut();
    });
  }

  handleLogOut() {
    this.auth.next(LOGGED_OUT);
    this.router.navigate(['login']);
  }
}

export class AuthContainer {
  username: string;
  role: string;
  isLoggedIn: boolean;
}

export const LOGGED_OUT: AuthContainer = {
  username: '',
  role: '',
  isLoggedIn: false,
};


class ChangePasswordContainer {
  oldPassword: string;
  newPassword: string;
}
