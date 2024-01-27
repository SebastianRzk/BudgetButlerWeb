import {Component, inject, OnInit} from '@angular/core';
import {Dauerauftrag,  GemeinsamerDauerauftrag} from '../../domain/model';
import { Observable } from 'rxjs';
import {GemeinsameDauerauftraegeService} from '../../domain/gemeinsame-dauerauftraege.service';

@Component({
  selector: 'app-allebuchungen',
  templateUrl: './gemeinsame-dauerauftraege.component.html',
  styleUrls: ['./gemeinsame-dauerauftraege.component.css']
})
export class GemeinsameDauerauftraegeComponent implements OnInit {
  displayedColumns: string[] = ['Eigenschaften', 'Aktion'];

  gemeinsameDauerauftrageService: GemeinsameDauerauftraegeService = inject(GemeinsameDauerauftraegeService);

  dauerauftraege: Observable<GemeinsamerDauerauftrag[]> = this.gemeinsameDauerauftrageService.gemeinsameDauerauftrage$;


  ngOnInit(): void {
    this.gemeinsameDauerauftrageService.refresh();
  }

  delete(dauerauftrag: Dauerauftrag) {
    this.gemeinsameDauerauftrageService.delete(dauerauftrag);
  }

  gleichesJahr(left: Date, right: Date){
    return left.getFullYear() === right.getFullYear();
  }
}
