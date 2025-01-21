import { Component, inject, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from '../auth.service';
import {ADD_SCHNELLEINSTIEG_ROUTE} from '../../../app-routes';
import { skip, take} from 'rxjs/operators';
import { MatButton } from '@angular/material/button';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css'],
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatButton]
})
export class LoginComponent implements OnInit {

  private authService: AuthService = inject(AuthService);
  private router: Router = inject(Router);


  ngOnInit() {
    this.authService.auth$.pipe(skip(1)).pipe(take(1)).subscribe(status => {
      if (status.loggedIn) {
        this.router.navigate([ADD_SCHNELLEINSTIEG_ROUTE]);
      } else {
        window.location.href = '/api/login/oauth2/authorization/oidc';
      }
    });
    this.authService.checkLoginState();
  }

}
