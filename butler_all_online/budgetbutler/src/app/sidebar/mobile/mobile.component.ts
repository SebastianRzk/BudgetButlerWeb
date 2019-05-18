import { Component, OnInit } from '@angular/core';
import { MenuitemService } from '../../menuitem.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-mobile-sidebar',
  templateUrl: './mobile.component.html',
  styleUrls: ['./mobile.component.css']
})
export class MobileComponent implements OnInit {

  public menuOpened = false;
  public menu = [];

  constructor(private menuitemService: MenuitemService, private router: Router) { }

  ngOnInit() {
    this.menu = this.menuitemService.getFlat();
  }

  toggleMenu() {
    this.menuOpened = !this.menuOpened;
  }

  navigateTo(url: string){
    this.router.navigate([url]);
  }
}
