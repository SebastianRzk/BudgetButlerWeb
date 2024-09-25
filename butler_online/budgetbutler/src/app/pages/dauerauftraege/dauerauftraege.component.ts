import {Component, inject, OnInit} from '@angular/core';
import {Dauerauftrag} from '../../domain/model';
import { Observable } from 'rxjs';
import {DauerauftraegeService} from "../../domain/dauerauftraege.service";
import { MatIcon } from '@angular/material/icon';
import { NgIf, DecimalPipe, DatePipe } from '@angular/common';
import { MatChipListbox, MatChip } from '@angular/material/chips';
import { MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow } from '@angular/material/table';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';

@Component({
    selector: 'app-allebuchungen',
    templateUrl: './dauerauftraege.component.html',
    styleUrls: ['./dauerauftraege.component.css'],
    standalone: true,
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatChipListbox, NgIf, MatChip, MatIcon, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow, DecimalPipe, DatePipe]
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
