import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { EinzelbuchungserviceService } from '../einzelbuchungservice.service';
import { KategorieService } from '../kategorie.service';
import { NotEmptyErrorStateMatcher } from '../matcher';
import { Einzelbuchung, GemeinsameBuchungAnlegen } from '../model';
import { Observable } from 'rxjs';
import { PartnerService } from '../partner.service';
import { GemeinsamebuchungService } from '../gemeinsamebuchung.service';


@Component({
  selector: 'app-addgemeinsameausgabe',
  templateUrl: './addgemeinsameausgabe.component.html',
  styleUrls: ['./addgemeinsameausgabe.component.css']
})
export class AddgemeinsameausgabeComponent implements OnInit {

  datum = new FormControl(new Date(), Validators.required);
  name = new FormControl('', Validators.required);
  kategorie = new FormControl('', Validators.required);
  kategorien: Observable<string[]>;
  wert = new FormControl('', Validators.required);
  person = new FormControl('', Validators.required);
  personen: Promise<string[]>;
  einzelbuchungMatcher = new NotEmptyErrorStateMatcher();

  constructor(
    private gemeinsameBuchungenService: GemeinsamebuchungService,
    private kategorieService: KategorieService,
    private partnerService: PartnerService) { }

  ngOnInit() {
    this.kategorien = this.kategorieService.getAll();
    this.personen = this.partnerService.getPartnerNames();
    this.personen.then(data => this.person.setValue(data[0]));
  }

  private isFormOk(): boolean {
    return !this.einzelbuchungMatcher.isErrorState(this.datum, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.name, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.kategorie, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.person, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.wert, null);
  }

  hinzufuegen() {
    if (! this.isFormOk()) {
      return;
    }

    const neueBuchung: GemeinsameBuchungAnlegen = {
      name: this.name.value,
      datum: this.datum.value,
      kategorie: this.kategorie.value,
      wert: this.wert.value * -1,
      zielperson: this.person.value
    };

    this.datum.reset(new Date());
    this.name.reset();
    this.kategorie.reset(this.kategorien[0]);
    this.wert.reset();
    this.gemeinsameBuchungenService.save(neueBuchung);
  }
}
