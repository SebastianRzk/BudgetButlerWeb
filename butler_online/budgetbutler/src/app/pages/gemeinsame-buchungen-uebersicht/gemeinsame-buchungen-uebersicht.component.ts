import {Component, inject, OnInit} from '@angular/core';
import {BuchungsUebersicht} from '../../domain/model';
import {Observable} from 'rxjs';
import {AsyncPipe} from '@angular/common';
import {GemeinsameBuchungenUebersichtService} from "../../domain/gemeinsame-buchungen-uebersicht.service";
import {AusgabenUebersichtComponent} from "../components/ausgaben-uebersicht/ausgaben-uebersicht.component";

@Component({
  selector: 'app-gemeinsame-buchungen-uebersicht',
  templateUrl: './gemeinsame-buchungen-uebersicht.component.html',
  styleUrls: ['./gemeinsame-buchungen-uebersicht.component.css'],
  imports: [AsyncPipe, AusgabenUebersichtComponent]
})
export class GemeinsameBuchungenUebersichtComponent implements OnInit {
  private uebersichtService: GemeinsameBuchungenUebersichtService = inject(GemeinsameBuchungenUebersichtService);
  uebersicht$: Observable<BuchungsUebersicht> = this.uebersichtService.gemeinsameBuchungenUebersicht$;

  ngOnInit(): void {
    this.uebersichtService.refresh();
  }
}
