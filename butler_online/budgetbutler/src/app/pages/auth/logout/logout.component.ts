import { Component, inject, OnInit } from '@angular/core';
import {AuthService} from '../auth.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {

  private authService: AuthService = inject(AuthService);

  ngOnInit() {
    this.authService.callLogout().subscribe(
      s => {
        if (s.logoutUrl) {
          window.location.href = s.logoutUrl;
        }
      }
    );
  }

  toLogin() {
    return this.authService.handleLogOut();
  }
}
