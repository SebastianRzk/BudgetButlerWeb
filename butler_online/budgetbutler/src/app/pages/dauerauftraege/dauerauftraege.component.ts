import {Component, inject, OnInit} from '@angular/core';
import {Dauerauftrag} from '../../domain/model';
import { Observable } from 'rxjs';
import {DauerauftraegeService} from "../../domain/dauerauftraege.service";

@Component({
  selector: 'app-allebuchungen',
  templateUrl: './dauerauftraege.component.html',
  styleUrls: ['./dauerauftraege.component.css']
})
export class DauerauftraegeComponent implements OnInit {
  displayedColumns: string[] = ['Eigenschaften', 'Aktion'];

  dauerauftragService: DauerauftraegeService = inject(DauerauftraegeService);

  dauerauftraege: Observable<Dauerauftrag[]> = this.dauerauftragService.dauerauftraege$;


  ngOnInit(): void {
    this.dauerauftragService.refresh();
  }

  delete(dauerauftrag: Dauerauftrag) {
    this.dauerauftragService.delete(dauerauftrag);
  }

  gleichesJahr(left: Date, right: Date){
    return left.getFullYear() == right.getFullYear();
  }
}
