import { Component, OnInit, Input } from '@angular/core';
import { MenuitemService } from 'src/app/menuitem.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-more',
  templateUrl: './more.component.html',
  styleUrls: ['./more.component.css']
})
export class MoreComponent implements OnInit {
  public menuOpened = false;
  public menu = [];

  @Input()
  public closeParent: () => void;


  constructor(private menuitemService: MenuitemService, private router: Router) { }

  ngOnInit() {
    this.menu = this.menuitemService.getAdditionalMobileMenuElements();
  }

  navigateTo(url: string){
    this.menuOpened = false;
    this.closeParent();
    this.router.navigate([url]);
  }


  toggleMenu = () => {
    this.menuOpened = !this.menuOpened;
  }

}
