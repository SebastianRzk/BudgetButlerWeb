import { Component, inject, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { GemeinsamebuchungService } from '../../domain/gemeinsamebuchung.service';
import { GemeinsameBuchung } from '../../domain/model';
import { NgIf, AsyncPipe, DecimalPipe, DatePipe } from '@angular/common';
import { MatIcon } from '@angular/material/icon';
import { MatChipListbox, MatChip, MatChipAvatar } from '@angular/material/chips';
import { MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow } from '@angular/material/table';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';

@Component({
    selector: 'app-allegemeinsamebuchungen',
    templateUrl: './allegemeinsamebuchungen.component.html',
    styleUrls: ['./allegemeinsamebuchungen.component.css'],
    standalone: true,
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatChipListbox, MatChip, MatIcon, MatChipAvatar, NgIf, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow, AsyncPipe, DecimalPipe, DatePipe]
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
