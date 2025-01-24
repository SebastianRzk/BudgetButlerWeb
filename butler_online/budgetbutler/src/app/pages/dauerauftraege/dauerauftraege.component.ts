import { Component, inject, OnInit } from '@angular/core';
import { Dauerauftrag } from '../../domain/model';
import { Observable } from 'rxjs';
import { DauerauftraegeService } from "../../domain/dauerauftraege.service";
import { MatIcon } from '@angular/material/icon';
import { DatePipe, DecimalPipe, NgIf } from '@angular/common';
import { MatChip, MatChipListbox } from '@angular/material/chips';
import {
  MatCell, MatCellDef,
  MatColumnDef,
  MatHeaderCell,
  MatHeaderCellDef,
  MatHeaderRow, MatHeaderRowDef,
  MatRow, MatRowDef,
  MatTable
} from '@angular/material/table';
import { MatCard, MatCardContent, MatCardHeader, MatCardTitle } from '@angular/material/card';

@Component({
    selector: 'app-allebuchungen',
    templateUrl: './dauerauftraege.component.html',
    styleUrls: ['./dauerauftraege.component.css'],
  imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatTable, MatColumnDef, MatHeaderCell, MatCell, MatChipListbox, NgIf, MatChip, MatIcon, MatHeaderRow, MatRow, DecimalPipe, DatePipe, MatHeaderCellDef, MatCellDef, MatHeaderRowDef, MatRowDef]
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
