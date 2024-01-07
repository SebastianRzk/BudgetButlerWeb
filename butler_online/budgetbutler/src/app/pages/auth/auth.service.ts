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
        this.notificationService.log(ERROR_LOGIN_RESULT, 'Login fehlgeschlagen');
        this.auth.next(LOGGED_OUT);
      }
    );
  }

  checkLoginState() {
    this.httpClient.get<AuthContainer | null>(this.api.getUrl('login/user')).subscribe(
      data => {
        if (data != null && data.loggedIn) {
          this.auth.next(
            {
              userName: data.userName,
              loggedIn: true
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

  public getLogin: () => Observable<AuthContainer> = () => this.httpClient.get<AuthContainer>(this.api.getUrl('login/user'));


  logout(): void {
    this.httpClient.get<null>(this.api.getUrl('logout')).subscribe(() => {
      this.handleLogOut();
    });
  }

  handleLogOut() {
    this.auth.next(LOGGED_OUT);
    this.router.navigate(['login']);
  }
}

export class AuthContainer {
  userName: string;
  loggedIn: boolean;
}

export const LOGGED_OUT: AuthContainer = {
  userName: '',
  loggedIn: false,
};
