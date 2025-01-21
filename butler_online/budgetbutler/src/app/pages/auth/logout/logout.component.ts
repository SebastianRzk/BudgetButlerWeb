import { Component, inject, OnInit } from '@angular/core';
import {AuthService} from '../auth.service';
import { MatButton } from '@angular/material/button';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';

@Component({
    selector: 'app-logout',
    templateUrl: './logout.component.html',
    styleUrls: ['./logout.component.css'],
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatButton]
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
