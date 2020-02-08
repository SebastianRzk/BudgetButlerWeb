import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
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

  buchungForm = new FormGroup({
    datum: new FormControl(new Date(), Validators.required),
    name: new FormControl('', Validators.required),
    kategorie: new FormControl('', Validators.required),
    wert: new FormControl('', Validators.required),
    person: new FormControl('', Validators.required),
  });

  kategorien: Observable<string[]>;
  personen: Promise<string[]>;

  constructor(
    private gemeinsameBuchungenService: GemeinsamebuchungService,
    private kategorieService: KategorieService,
    private partnerService: PartnerService) { }

  ngOnInit() {
    this.kategorien = this.kategorieService.getAll();
    this.personen = this.partnerService.getPartnerNames();
    this.personen.then(data => this.buchungForm.get('person').setValue(data[0]));
  }

  onFormSubmit() {
    if (!this.buchungForm.valid) {
      return;
    }

    const neueBuchung: GemeinsameBuchungAnlegen = {
      name: this.buchungForm.get('name').value,
      datum: this.buchungForm.get('datum').value,
      kategorie: this.buchungForm.get('kategorie').value,
      wert: this.buchungForm.get('wert').value * -1,
      zielperson: this.buchungForm.get('person').value
    };
    this.gemeinsameBuchungenService.save(neueBuchung);
    this.buchungForm.reset({datum: new Date()})
  }
}
