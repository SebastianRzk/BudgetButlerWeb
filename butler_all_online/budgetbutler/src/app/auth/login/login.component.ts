import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  hide = true;
  email = '';
  password = '';

  constructor(public authService: AuthService, public router: Router) {}


  ngOnInit() {
    this.authService.checkLoginState().subscribe(() => {});
  }

  login() {
    this.authService.login(this.email, this.password).subscribe(() => {});
  }
}
