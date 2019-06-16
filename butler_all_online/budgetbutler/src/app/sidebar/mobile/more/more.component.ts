import { Component, OnInit } from '@angular/core';
import { MenuitemService } from 'src/app/menuitem.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-more',
  templateUrl: './more.component.html',
  styleUrls: ['./more.component.css']
})
export class MoreComponent implements OnInit {
  more: boolean = false;
  public menuOpened = false;
  public menu = [];

  constructor(private menuitemService: MenuitemService, private router: Router) { }

  ngOnInit() {
    this.menu = this.menuitemService.getAdditionalMobileMenuElements();
  }

  navigateTo(url: string){
    this.menuOpened = false;
    this.router.navigate([url]);
  }


  toggleMenu = () => {
    this.more = !this.more;
  }

}
