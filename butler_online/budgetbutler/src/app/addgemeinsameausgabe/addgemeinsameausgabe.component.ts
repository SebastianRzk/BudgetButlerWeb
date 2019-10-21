import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { GemeinsamebuchungService } from '../gemeinsamebuchung.service';
import { KategorieService } from '../kategorie.service';
import { MyErrorStateMatcher } from '../matcher';
import { GemeinsameBuchungAnlegen } from '../model';
import { PartnerService } from '../partner.service';


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
  einzelbuchungMatcher = new MyErrorStateMatcher();

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
    return this.datum.valid &&
      this.name.valid &&
      this.kategorie.valid &&
      this.person.valid &&
      this.wert.valid;
  }

  hinzufuegen() {
    if (!this.isFormOk()) {
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
