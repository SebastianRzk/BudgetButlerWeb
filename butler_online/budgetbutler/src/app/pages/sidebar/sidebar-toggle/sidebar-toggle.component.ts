import { Component, inject } from '@angular/core';
import { MenuItemService } from '../../../domain/menu-item.service';
import { AuthService } from '../../auth/auth.service';
import { MatIcon } from '@angular/material/icon';
import { MatButton } from '@angular/material/button';
import { AsyncPipe } from '@angular/common';

@Component({
    selector: 'app-sidebar-toggle',
    templateUrl: './sidebar-toggle.component.html',
    styleUrls: ['./sidebar-toggle.component.css'],
  imports: [MatButton, MatIcon, AsyncPipe]
})
export class SidebarToggleComponent {
  public menuService: MenuItemService = inject(MenuItemService);
  public authService: AuthService = inject(AuthService);
}
