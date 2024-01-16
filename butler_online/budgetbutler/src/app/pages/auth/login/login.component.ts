import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from '../auth.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {ADD_SCHNELLEINSTIEG_ROUTE} from '../../../app-routes';
import {debounce, skip, take} from 'rxjs/operators';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {


  constructor(public authService: AuthService, public router: Router) {
  }


  ngOnInit() {
    this.authService.auth$.pipe(skip(1)).pipe(take(1)).subscribe(status => {
      if (status.loggedIn) {
        this.router.navigate([ADD_SCHNELLEINSTIEG_ROUTE]);
      } else {
        window.location.href = "/api/login/oauth2/authorization/oidc";
      }
    });
    this.authService.checkLoginState();
  }

}
