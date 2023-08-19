import {Component} from '@angular/core';
import {MenuitemService} from '../../../domain/menuitem.service';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {AuthContainer, AuthService} from '../../auth/auth.service';

@Component({
  selector: 'app-sidebar-toggle',
  templateUrl: './sidebar-toggle.component.html',
  styleUrls: ['./sidebar-toggle.component.css']
})
export class SidebarToggleComponent {

  closed$: Observable<boolean>;
  user$: Observable<AuthContainer>;

  constructor(public menuService: MenuitemService, authService: AuthService) {
    this.closed$ = menuService.opened$.pipe(map(x => !x));
    this.user$ = authService.auth$;
  }

}
