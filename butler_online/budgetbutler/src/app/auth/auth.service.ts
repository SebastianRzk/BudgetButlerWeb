import { Injectable } from '@angular/core';

import { tap } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ApiproviderService } from '../apiprovider.service';
import { NotificationService } from '../notification.service';
import { Result, ERROR_LOGIN_RESULT } from '../model';
import { Observable } from 'rxjs';
import { ADD_SCHNELLEINSTIEG_ROUTE } from '../app-routes';





@Injectable({
  providedIn: 'root',
})
export class AuthService {
  isLoggedIn = false;
  username = '';
  authToken: AuthContainer;
  redirectUrl = '';

  constructor(private httpClient: HttpClient, private router: Router, private api: ApiproviderService, private notificationService: NotificationService) {
  }

  login(username: string, password: string) {
    const body = new FormData();
    body.append('email', username);
    body.append('password', password);

    return this.httpClient.post<AuthContainer>(this.api.getUrl('login.php'), body).pipe(
      tap(
        data => {
          if (data != null) {
            this.isLoggedIn = true;
            this.username = data.username;
            this.router.navigate([ADD_SCHNELLEINSTIEG_ROUTE]);
          } else {
            this.notificationService.log(ERROR_LOGIN_RESULT, 'Login');
            this.isLoggedIn = false;
          }
        },
        error => {
          this.notificationService.log(ERROR_LOGIN_RESULT, 'Login fehlgeschlagen');
          this.isLoggedIn = false;
        }
      ));
  }

  checkLoginState() {
    return this.httpClient.get<AuthContainer>(this.api.getUrl('login.php')).pipe(
      tap(
        data => {
          if (data != null) {
            this.isLoggedIn = true;
            this.username = data.username;
            if (this.redirectUrl) {
              this.router.navigate([this.redirectUrl]);
            } else {
              this.router.navigate([ADD_SCHNELLEINSTIEG_ROUTE]);
            }
          } else {
            this.isLoggedIn = false;
          }
        },
        error => {
          console.log('Mischt', error);
          this.isLoggedIn = false;
        }
      ));
  }

  public getLogin: () => Observable<AuthContainer> = () => this.httpClient.get<AuthContainer>(this.api.getUrl('login.php'));


  changePassword(oldPassword: string, newPassword: string) {
    const body: ChangePasswordContainer = {
      oldPassword: oldPassword,
      newPassword: newPassword
    };
    return this.httpClient.post<Result>(this.api.getUrl('changepassword.php'), body).
      toPromise().then(
        data => {
          this.notificationService.handleServerResult(data, 'Passwort ändern');
        },
        error => {
          console.log('Mischt', error);
          this.isLoggedIn = false;
        }
      );
  }


  isAdmin = () => this.username === 'admin';

  logout(): void {
    this.httpClient.get(this.api.getUrl('logout.php')).toPromise().then(() => {
      this.isLoggedIn = false;
      this.router.navigate(['login']);
    });
    this.isLoggedIn = false;
  }
}

export class AuthContainer {
  username: string;
  role: string;
}


class ChangePasswordContainer {
  oldPassword: string;
  newPassword: string;
}
