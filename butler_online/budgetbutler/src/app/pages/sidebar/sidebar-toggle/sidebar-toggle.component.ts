import { Component, inject } from '@angular/core';
import { MenuItemService } from '../../../domain/menu-item.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AuthContainer, AuthService } from '../../auth/auth.service';
import { MatIcon } from '@angular/material/icon';
import { MatButton } from '@angular/material/button';
import { NgIf, AsyncPipe } from '@angular/common';

@Component({
    selector: 'app-sidebar-toggle',
    templateUrl: './sidebar-toggle.component.html',
    styleUrls: ['./sidebar-toggle.component.css'],
    imports: [NgIf, MatButton, MatIcon, AsyncPipe]
})
export class SidebarToggleComponent {

  public menuService: MenuItemService = inject(MenuItemService);
  private authService: AuthService = inject(AuthService);

  closed$: Observable<boolean> = this.menuService.opened$.pipe(map(x => !x));
  user$: Observable<AuthContainer> = this.authService.auth$;


}
