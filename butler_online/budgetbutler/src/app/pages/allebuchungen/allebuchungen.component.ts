import {Component, inject, OnInit} from '@angular/core';
import {EinzelbuchungService as EinzelbuchungService} from '../../domain/einzelbuchung.service';
import {Einzelbuchung} from '../../domain/model';
import {Observable} from 'rxjs';
import {DatePipe, DecimalPipe} from '@angular/common';
import {MatIcon} from '@angular/material/icon';
import {MatChip, MatChipListbox} from '@angular/material/chips';
import {
  MatCell, MatCellDef,
  MatColumnDef,
  MatHeaderCell,
  MatHeaderCellDef,
  MatHeaderRow, MatHeaderRowDef,
  MatRow, MatRowDef,
  MatTable
} from '@angular/material/table';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle} from '@angular/material/card';

@Component({
  selector: 'app-allebuchungen',
  templateUrl: './allebuchungen.component.html',
  styleUrls: ['./allebuchungen.component.css'],
  imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatTable, MatColumnDef, MatHeaderCell, MatCell, MatChipListbox, MatChip, MatIcon, MatHeaderRow, MatRow, DecimalPipe, DatePipe, MatHeaderCellDef, MatCellDef, MatHeaderRowDef, MatRowDef]
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
