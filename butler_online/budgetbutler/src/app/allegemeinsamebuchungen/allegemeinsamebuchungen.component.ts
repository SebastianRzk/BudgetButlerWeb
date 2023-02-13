import {Component, OnInit} from '@angular/core';
import {Observable} from 'rxjs';
import {GemeinsamebuchungService} from '../gemeinsamebuchung.service';
import {GemeinsameBuchung} from '../model';

@Component({
  selector: 'app-allegemeinsamebuchungen',
  templateUrl: './allegemeinsamebuchungen.component.html',
  styleUrls: ['./allegemeinsamebuchungen.component.css']
})
export class AllegemeinsamebuchungenComponent implements OnInit {


  displayedColumns: string[] = ['Datum', 'Eigenschaften', 'Aktion'];
  gemeinsamebuchungen: Observable<GemeinsameBuchung[]>;

  constructor(private gemeinsameBuchungenService: GemeinsamebuchungService) {
    this.gemeinsamebuchungen = this.gemeinsameBuchungenService.gemeinsameBuchungen$;
  }

  ngOnInit(): void {
    this.loadData();
  }

  loadData() {
    this.gemeinsameBuchungenService.refresh();
  }


  toLocaleShortString(date: string) {
    const datum = new Date(date);
    return datum.getDate() + '.' + (datum.getMonth() + 1);
  }

  delete(buchung: GemeinsameBuchung) {
    this.gemeinsameBuchungenService.delete({id: buchung.id});
  }

  personIsOther(buchung: GemeinsameBuchung) {
    return buchung.zielperson !== buchung.user;
  }
}
