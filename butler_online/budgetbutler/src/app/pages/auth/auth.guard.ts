import {Injectable} from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';

import {AuthService} from './auth.service';
import { map, skip, take } from 'rxjs/operators';
import {LOGIN_ROUTE} from '../../app-routes';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {
  }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> {
    this.authService.checkLoginState();
    return this.authService.auth$.pipe(skip(1)).pipe(take(1)).pipe(map(
      auth => {
        console.log(auth);
        if (!auth.loggedIn) {
          console.log('routing away');
          this.router.navigate([LOGIN_ROUTE]);
          return false;
        }
        return true;
      })
    );
  }

}
