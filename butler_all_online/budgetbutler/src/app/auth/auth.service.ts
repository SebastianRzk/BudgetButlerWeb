import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';
import { tap, delay } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { ApiproviderService } from '../apiprovider.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  isLoggedIn = false;
  username = '';
  authToken: AuthContainer;
  redirectUrl = '';

  constructor(private httpClient: HttpClient, private router: Router, private api: ApiproviderService) {
  }

  login(username: string, password: string) {
    const body = new FormData();
    body.append('email', username);
    body.append('password', password);

    return this.httpClient.post<AuthContainer>(this.api.getUrl('login.php'), body).pipe(
      tap( // Log the result or error
        data => {
          if (data != null && 'token' in data ) {
            this.isLoggedIn = true;
            this.username = data.username;
            this.router.navigate(['dashboard']);
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

  checkLoginState() {
    return this.httpClient.get<AuthContainer>(this.api.getUrl('login.php')).pipe(
      tap( // Log the result or error
        data => {
          if (data != null && 'token' in data ) {
            this.isLoggedIn = true;
            this.router.navigate(['dashboard']);
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

  logout(): void {
    this.httpClient.get(this.api.getUrl('logout.php')).subscribe(() => {
      this.isLoggedIn = false;
      this.router.navigate([ 'login' ]);
  });
    this.isLoggedIn = false;
  }
}

class AuthContainer {
  token: string;
  username: string;
}
