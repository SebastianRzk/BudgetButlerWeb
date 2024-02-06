import { inject, Injectable } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { AuthContainer, AuthService } from './auth.service';
import { map, skip, take } from 'rxjs/operators';
import { LOGIN_ROUTE } from '../../app-routes';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard {
  private authService: AuthService = inject(AuthService);
  private router: Router = inject(Router);

  canActivate(): Observable<boolean> {
    const result: Observable<boolean> = this.authService.auth$.pipe(skip(1), take(1)).pipe(map(
      (auth: AuthContainer) => {
        if (!auth.loggedIn) {
          this.router.navigate([LOGIN_ROUTE]);
          return false;
        }
        return true;
      })
    );
    this.authService.checkLoginState();
    return result
  }
}

export const canActivateAuthGuard: CanActivateFn = () => inject(AuthGuard).canActivate()
