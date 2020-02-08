import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { Observable } from 'rxjs';
import { EinzelbuchungserviceService } from '../einzelbuchungservice.service';
import { KategorieService } from '../kategorie.service';
import { MyErrorStateMatcher } from '../matcher';
import { EinzelbuchungAnlegen } from '../model';


@Component({
  selector: 'app-addeinnahme',
  templateUrl: './addeinnahme.component.html',
  styleUrls: ['./addeinnahme.component.css']
})
export class AddeinnahmeComponent implements OnInit {

  buchungForm = new FormGroup({
    datum: new FormControl(new Date(), Validators.required),
    name: new FormControl('', Validators.required),
    kategorie: new FormControl('', Validators.required),
    wert: new FormControl('', Validators.required)
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
      wert: this.buchungForm.get('wert').value
    };
    this.einzelbuchungsService.save(neueBuchung);
    this.buchungForm.reset({ datum: new Date() })
  }
}
