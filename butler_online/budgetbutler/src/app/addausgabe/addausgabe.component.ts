import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { Observable } from 'rxjs';
import { EinzelbuchungserviceService } from '../einzelbuchungservice.service';
import { KategorieService } from '../kategorie.service';
import { EinzelbuchungAnlegen } from '../model';


@Component({
  selector: 'app-addausgabe',
  templateUrl: './addausgabe.component.html',
  styleUrls: ['./addausgabe.component.css']
})
export class AddausgabeComponent implements OnInit {

  buchungForm = new FormGroup({
    datum: new FormControl(new Date(), Validators.required),
    name: new FormControl('', Validators.required),
    kategorie: new FormControl('', Validators.required),
    wert: new FormControl('', Validators.required),
  });

  kategorien: Observable<string[]>;

  constructor(
    private einzelbuchungsService: EinzelbuchungserviceService,
    private kategorieService: KategorieService) { }

  ngOnInit() {
    this.kategorien = this.kategorieService.getAll();
  }

  onFormSubmit() {
    if (!this.buchungForm.valid) {
      return;
    }

    const neueBuchung: EinzelbuchungAnlegen = {
      name: this.buchungForm.get('name').value,
      datum: this.buchungForm.get('datum').value,
      kategorie: this.buchungForm.get('kategorie').value,
      wert: this.buchungForm.get('wert').value * -1
    };
    this.einzelbuchungsService.save(neueBuchung);
    this.buchungForm.reset({datum: new Date()});
  }
}
