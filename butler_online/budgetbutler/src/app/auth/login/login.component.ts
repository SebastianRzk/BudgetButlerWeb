import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm = new FormGroup({
    email: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required)
  })

  hide = true;

  constructor(public authService: AuthService, public router: Router) {}


  ngOnInit() {
    this.authService.checkLoginState().toPromise().then(() => {});
  }

  login() {
    if(!this.loginForm.valid){
      return
    }
    this.authService.login(this.loginForm.get('email').value, this.loginForm.get('password').value).toPromise().then(() => {});
  }
}
