import { Component, inject, OnInit } from '@angular/core';
import { Dauerauftrag, GemeinsamerDauerauftrag } from '../../domain/model';
import { Observable } from 'rxjs';
import { GemeinsameDauerauftraegeService } from '../../domain/gemeinsame-dauerauftraege.service';
import { MatIcon } from '@angular/material/icon';
import { DatePipe, DecimalPipe, NgIf } from '@angular/common';
import { MatChip, MatChipAvatar, MatChipListbox } from '@angular/material/chips';
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
    templateUrl: './gemeinsame-dauerauftraege.component.html',
    styleUrls: ['./gemeinsame-dauerauftraege.component.css'],
  imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatTable, MatColumnDef, MatHeaderCell, MatCell, MatChipListbox, NgIf, MatChip, MatIcon, MatChipAvatar, MatHeaderRow, MatRow, DecimalPipe, DatePipe, MatHeaderCellDef, MatCellDef, MatHeaderRowDef, MatRowDef]
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
