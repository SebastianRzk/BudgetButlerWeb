import {Component, inject, OnInit} from '@angular/core';
import {BuchungsUebersicht} from '../../domain/model';
import {Observable} from 'rxjs';
import {AsyncPipe} from '@angular/common';
import {EinzelbuchungUebersichtService} from "../../domain/einzelbuchung-uebersicht.service";
import {AusgabenUebersichtComponent} from "../components/ausgaben-uebersicht/ausgaben-uebersicht.component";

@Component({
  selector: 'app-buchungen-uebersicht',
  templateUrl: './persoenliche-buchungen-uebersicht.component.html',
  styleUrls: ['./persoenliche-buchungen-uebersicht.component.css'],
  imports: [AsyncPipe, AusgabenUebersichtComponent]
})
export class PersoenlicheBuchungenUebersichtComponent implements OnInit {
  private uebersichtService: EinzelbuchungUebersichtService = inject(EinzelbuchungUebersichtService);
  uebersicht$: Observable<BuchungsUebersicht> = this.uebersichtService.einzelbuchungenUebersicht$;

  ngOnInit(): void {
    this.uebersichtService.refresh();
  }
}
