import { Component, inject, OnInit } from '@angular/core';
import { EinzelbuchungService as EinzelbuchungService } from '../../domain/einzelbuchung.service';
import { Einzelbuchung } from '../../domain/model';
import { Observable } from 'rxjs';
import { DecimalPipe, DatePipe } from '@angular/common';
import { MatIcon } from '@angular/material/icon';
import { MatChipListbox, MatChip } from '@angular/material/chips';
import { MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow } from '@angular/material/table';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';

@Component({
    selector: 'app-allebuchungen',
    templateUrl: './allebuchungen.component.html',
    styleUrls: ['./allebuchungen.component.css'],
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatChipListbox, MatChip, MatIcon, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow, DecimalPipe, DatePipe]
})
export class AllebuchungenComponent implements OnInit {
  private einzelbuchungService: EinzelbuchungService = inject(EinzelbuchungService);
  displayedColumns: string[] = ['Datum', 'Eigenschaften', 'Aktion'];
  einzelbuchungen$: Observable<Einzelbuchung[]> = this.einzelbuchungService.einzelbuchungen$;

  ngOnInit(): void {
    this.einzelbuchungService.refresh();
  }

  delete(einzelbuchung: Einzelbuchung) {
    this.einzelbuchungService.delete(einzelbuchung);
  }
}
