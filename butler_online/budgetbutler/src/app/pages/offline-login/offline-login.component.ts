import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { MenuitemService } from "../../domain/menuitem.service";
import { BehaviorSubject, Observable } from "rxjs";

@Component({
  selector: 'app-offline-login',
  templateUrl: './offline-login.component.html',
  styleUrls: ['./offline-login.component.css']
})
export class OfflineLoginComponent implements OnInit {

  private disabledSubject = new BehaviorSubject(false);

  disabled$: Observable<boolean> = this.disabledSubject.asObservable();

  constructor(private authService: AuthService, private menuitemService: MenuitemService) {
  }


  ngOnInit() {
    this.menuitemService.close();
    this.authService.checkLoginState(true);
    this.authService.auth$.subscribe(
      element =>  this.disabledSubject.next(!element.loggedIn)
    );
  }

  navigate() {
    window.location.href = 'api/login/offline/access';
  }

}
;
