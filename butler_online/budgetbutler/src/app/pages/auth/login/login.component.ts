import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from '../auth.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {ADD_SCHNELLEINSTIEG_ROUTE} from '../../../app-routes';
import {take} from 'rxjs/operators';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm = new FormGroup({
    email: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required)
  });

  hide = true;


  constructor(public authService: AuthService, public router: Router) {
  }


  ngOnInit() {
    this.authService.auth$.pipe(take(2)).subscribe(status => {
      if (status.isLoggedIn) {
        this.router.navigate([ADD_SCHNELLEINSTIEG_ROUTE]);
      }
    });
    this.authService.checkLoginState();
  }


  login() {
    if (!this.loginForm.valid) {
      return;
    }
    this.authService.login(this.loginForm.get('email').value, this.loginForm.get('password').value);
  }
}
