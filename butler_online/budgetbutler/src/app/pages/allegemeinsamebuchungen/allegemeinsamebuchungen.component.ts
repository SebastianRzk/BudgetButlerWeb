import { Component, inject, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { GemeinsamebuchungService } from '../../domain/gemeinsamebuchung.service';
import { GemeinsameBuchung } from '../../domain/model';

@Component({
  selector: 'app-allegemeinsamebuchungen',
  templateUrl: './allegemeinsamebuchungen.component.html',
  styleUrls: ['./allegemeinsamebuchungen.component.css']
})
export class AllegemeinsamebuchungenComponent implements OnInit {
  private gemeinsameBuchungenService: GemeinsamebuchungService = inject(GemeinsamebuchungService);

  displayedColumns: string[] = ['Datum', 'Eigenschaften', 'Aktion'];
  gemeinsamebuchungen: Observable<GemeinsameBuchung[]> = this.gemeinsameBuchungenService.gemeinsameBuchungen$;

  ngOnInit(): void {
    this.gemeinsameBuchungenService.refresh();
  }

  delete(buchung: GemeinsameBuchung) {
    this.gemeinsameBuchungenService.delete({id: buchung.id});
  }

}
