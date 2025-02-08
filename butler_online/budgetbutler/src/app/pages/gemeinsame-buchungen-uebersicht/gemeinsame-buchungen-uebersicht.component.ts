import { Component, inject, OnInit } from '@angular/core';
import { BuchungsUebersicht } from '../../domain/model';
import { Observable } from 'rxjs';
import { AsyncPipe, DecimalPipe, KeyValuePipe } from '@angular/common';
import { MatCard, MatCardContent, MatCardHeader, MatCardTitle } from '@angular/material/card';
import { GemeinsameBuchungenUebersichtService } from "../../domain/gemeinsame-buchungen-uebersicht.service";

@Component({
  selector: 'app-gemeinsame-buchungen-uebersicht',
  templateUrl: './gemeinsame-buchungen-uebersicht.component.html',
  styleUrls: ['./gemeinsame-buchungen-uebersicht.component.css'],
  imports: [MatCard, MatCardTitle, MatCardContent, DecimalPipe, AsyncPipe, KeyValuePipe, MatCardHeader]
})
export class GemeinsameBuchungenUebersichtComponent implements OnInit {
  private uebersichtService: GemeinsameBuchungenUebersichtService = inject(GemeinsameBuchungenUebersichtService);
  uebersicht$: Observable<BuchungsUebersicht> = this.uebersichtService.gemeinsameBuchungenUebersicht$;

  ngOnInit(): void {
    this.uebersichtService.refresh();
  }
}
