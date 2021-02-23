import { Component, OnDestroy, OnInit } from '@angular/core';
import { Observable, Subscription } from 'rxjs';
import { EinzelbuchungserviceService as EinzelbuchungService } from '../einzelbuchungservice.service';
import { Einzelbuchung } from '../model';

@Component({
  selector: 'app-allebuchungen',
  templateUrl: './allebuchungen.component.html',
  styleUrls: ['./allebuchungen.component.css']
})
export class AllebuchungenComponent implements OnInit, OnDestroy {

  displayedColumns: string[] = ['Datum', 'Name', 'Kategorie', 'Wert', 'Aktion'];
  displayedMobileColumns: string[] = ['Datum', 'Eigenschaften', 'Aktion'];
  einzelbuchungen: Einzelbuchung[];
  subscription: Subscription;

  constructor(private einzelbuchungService: EinzelbuchungService) {
  }

  ngOnInit(): void {
    this.subscription = this.einzelbuchungService.getAll().subscribe(x => this.einzelbuchungen = x);
    this.refreshData();
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  refreshData = () => {
    this.einzelbuchungService.refresh();
  }

  toLocaleString = (date: string) => {
    return new Date(date).toLocaleDateString('de-DE');
  }

  toLocaleWert = (data: string) => {
    return Number(data).toFixed(2);
  }

  toLocaleShortString(date: string) {
    const datum = new Date(date);
    return datum.getDate() + '.' + (datum.getMonth() + 1);
  }

  delete(einzelbuchung: Einzelbuchung) {
    this.einzelbuchungService.delete(einzelbuchung);
    this.refreshData();
  }
}
