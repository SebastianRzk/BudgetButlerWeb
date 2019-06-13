import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { GemeinsamebuchungService } from '../gemeinsamebuchung.service';
import { GemeinsameBuchung } from '../model';
import { PartnerService, PartnerInfo } from '../partner.service';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-allegemeinsamebuchungen',
  templateUrl: './allegemeinsamebuchungen.component.html',
  styleUrls: ['./allegemeinsamebuchungen.component.css']
})
export class AllegemeinsamebuchungenComponent implements OnInit {


  displayedColumns: string[] = ['Datum', 'Name', 'Kategorie', 'Person', 'Wert', 'Aktion'];
  displayedMobileColumns: string[] = ['Datum', 'Eigenschaften', 'Aktion'];
  einzelbuchungen: Observable<GemeinsameBuchung[]>;
  partnerData: PartnerInfo;

  constructor(private gemeinsameBuchungenService: GemeinsamebuchungService, private partnerService: PartnerService) {
  }

  ngOnInit(): void {
    this.loadData();
  }

  loadData = () => {
    this.einzelbuchungen = this.gemeinsameBuchungenService.getAll();
    this.partnerService.getPartnerInfo().pipe(first()).toPromise().then(
      partnerData => this.partnerData = partnerData
    )
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

  isEditable = (buchung: GemeinsameBuchung) => {
    if(! this.partnerData){
      return false;
    }
    if(buchung.user !== this.partnerData.partnername){
      return true;
    }
    return this.partnerData.erweiterteRechteBekommen;
  }
}
