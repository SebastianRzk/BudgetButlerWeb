import {Component, inject, OnInit} from '@angular/core';
import {Dauerauftrag,  GemeinsamerDauerauftrag} from '../../domain/model';
import { Observable } from 'rxjs';
import {GemeinsameDauerauftraegeService} from '../../domain/gemeinsame-dauerauftraege.service';
import { MatIcon } from '@angular/material/icon';
import { NgIf, DecimalPipe, DatePipe } from '@angular/common';
import { MatChipListbox, MatChip, MatChipAvatar } from '@angular/material/chips';
import { MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow } from '@angular/material/table';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';

@Component({
    selector: 'app-allebuchungen',
    templateUrl: './gemeinsame-dauerauftraege.component.html',
    styleUrls: ['./gemeinsame-dauerauftraege.component.css'],
    standalone: true,
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatChipListbox, NgIf, MatChip, MatIcon, MatChipAvatar, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow, DecimalPipe, DatePipe]
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
