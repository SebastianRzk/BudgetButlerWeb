import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { GemeinsamebuchungService } from '../gemeinsamebuchung.service';
import { GemeinsameBuchung } from '../model';

@Component({
  selector: 'app-allegemeinsamebuchungen',
  templateUrl: './allegemeinsamebuchungen.component.html',
  styleUrls: ['./allegemeinsamebuchungen.component.css']
})
export class AllegemeinsamebuchungenComponent implements OnInit, OnDestroy {


  displayedColumns: string[] = ['Datum', 'Name', 'Kategorie', 'Person', 'Wert', 'Aktion'];
  displayedMobileColumns: string[] = ['Datum', 'Eigenschaften', 'Aktion'];
  gemeinsamebuchungen: GemeinsameBuchung[];
  private subscription: Subscription;

  constructor(private gemeinsameBuchungenService: GemeinsamebuchungService) {
  }

  ngOnInit(): void {
    this.subscription = this.gemeinsameBuchungenService.getAll().subscribe(x => this.gemeinsamebuchungen = x);
    this.loadData();
  }

  loadData = () => {
    this.gemeinsameBuchungenService.refresh();
  }

  ngOnDestroy = () => {
    this.subscription.unsubscribe();
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

  delete(buchung: GemeinsameBuchung) {
    this.gemeinsameBuchungenService.delete({ id: buchung.id });
    this.loadData();
  }

  generatePerson = (buchung: GemeinsameBuchung) => {
    if (!this.personIsOther(buchung)) {
      return buchung.user;
    }
    return `${buchung.zielperson} (von ${buchung.user})`;
  }

  personIsOther = (buchung: GemeinsameBuchung) => {
    return buchung.zielperson !== buchung.user;
  }
}
