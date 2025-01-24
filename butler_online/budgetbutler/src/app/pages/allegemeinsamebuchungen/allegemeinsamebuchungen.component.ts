import { Component, inject, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { GemeinsamebuchungService } from '../../domain/gemeinsamebuchung.service';
import { GemeinsameBuchung } from '../../domain/model';
import { DatePipe, DecimalPipe, NgIf } from '@angular/common';
import { MatIcon } from '@angular/material/icon';
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
  selector: 'app-allegemeinsamebuchungen',
  templateUrl: './allegemeinsamebuchungen.component.html',
  styleUrls: ['./allegemeinsamebuchungen.component.css'],
  imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatTable, MatColumnDef, MatHeaderCell, MatCell, MatChipListbox, MatChip, MatIcon, MatChipAvatar, NgIf, MatHeaderRow, MatRow, DecimalPipe, DatePipe, MatHeaderCellDef, MatCellDef, MatHeaderRowDef, MatRowDef]
})
export class AllegemeinsamebuchungenComponent implements OnInit {
  private gemeinsameBuchungenService: GemeinsamebuchungService = inject(GemeinsamebuchungService);

  displayedColumns: string[] = ['Datum', 'Eigenschaften', 'Aktion'];
  gemeinsamebuchungen$: Observable<GemeinsameBuchung[]> = this.gemeinsameBuchungenService.gemeinsameBuchungen$;

  ngOnInit(): void {
    this.gemeinsameBuchungenService.refresh();
  }

  delete(buchung: GemeinsameBuchung) {
    this.gemeinsameBuchungenService.delete({id: buchung.id});
  }

}
