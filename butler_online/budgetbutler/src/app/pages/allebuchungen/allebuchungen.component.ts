import { Component, inject, OnInit } from '@angular/core';
import { EinzelbuchungService as EinzelbuchungService } from '../../domain/einzelbuchung.service';
import { Einzelbuchung } from '../../domain/model';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-allebuchungen',
  templateUrl: './allebuchungen.component.html',
  styleUrls: ['./allebuchungen.component.css']
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
