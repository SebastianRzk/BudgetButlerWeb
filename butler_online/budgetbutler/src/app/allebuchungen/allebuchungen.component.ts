import {Component, OnInit} from '@angular/core';
import {EinzelbuchungService as EinzelbuchungService} from '../einzelbuchung.service';
import {Einzelbuchung} from '../model';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-allebuchungen',
  templateUrl: './allebuchungen.component.html',
  styleUrls: ['./allebuchungen.component.css']
})
export class AllebuchungenComponent implements OnInit {
  displayedColumns: string[] = ['Datum', 'Eigenschaften', 'Aktion'];
  einzelbuchungen: Observable<Einzelbuchung[]>;

  constructor(private einzelbuchungService: EinzelbuchungService) {
  }

  ngOnInit(): void {
    this.einzelbuchungen = this.einzelbuchungService.einzelbuchungen$;
    this.refreshData();
  }

  refreshData() {
    this.einzelbuchungService.refresh();
  }

  toLocaleShortString(date: string) {
    const datum = new Date(date);
    return datum.getDate() + '.' + (datum.getMonth() + 1);
  }

  delete(einzelbuchung: Einzelbuchung) {
    this.einzelbuchungService.delete(einzelbuchung);
  }
}
