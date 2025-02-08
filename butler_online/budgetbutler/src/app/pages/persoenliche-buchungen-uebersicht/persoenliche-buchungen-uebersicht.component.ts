import { Component, inject, OnInit } from '@angular/core';
import { BuchungsUebersicht } from '../../domain/model';
import { Observable } from 'rxjs';
import { AsyncPipe, DecimalPipe, KeyValuePipe } from '@angular/common';
import { MatCard, MatCardContent, MatCardHeader, MatCardTitle } from '@angular/material/card';
import { EinzelbuchungUebersichtService } from "../../domain/einzelbuchung-uebersicht.service";

@Component({
  selector: 'app-buchungen-uebersicht',
  templateUrl: './persoenliche-buchungen-uebersicht.component.html',
  styleUrls: ['./persoenliche-buchungen-uebersicht.component.css'],
  imports: [MatCard, MatCardTitle, MatCardContent, DecimalPipe, AsyncPipe, KeyValuePipe, MatCardHeader]
})
export class PersoenlicheBuchungenUebersichtComponent implements OnInit {
  private uebersichtService: EinzelbuchungUebersichtService = inject(EinzelbuchungUebersichtService);
  uebersicht$: Observable<BuchungsUebersicht> = this.uebersichtService.einzelbuchungenUebersicht$;

  ngOnInit(): void {
    this.uebersichtService.refresh();
  }
}
