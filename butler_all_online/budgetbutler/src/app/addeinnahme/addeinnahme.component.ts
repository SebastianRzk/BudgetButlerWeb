import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { EinzelbuchungserviceService } from '../einzelbuchungservice.service';
import { KategorieService } from '../kategorie.service';
import { NotEmptyErrorStateMatcher } from '../matcher';
import { Einzelbuchung, EinzelbuchungAnlegen } from '../model';
import { Observable } from 'rxjs';


@Component({
  selector: 'app-addeinnahme',
  templateUrl: './addeinnahme.component.html',
  styleUrls: ['./addeinnahme.component.css']
})
export class AddeinnahmeComponent implements OnInit {

  datum = new FormControl(new Date(), Validators.required);
  name = new FormControl('', Validators.required);
  kategorie = new FormControl('', Validators.required);
  kategorien: Observable<string[]>;
  wert = new FormControl('', Validators.required);
  einzelbuchungMatcher = new NotEmptyErrorStateMatcher();

  constructor(
    private einzelbuchungsService: EinzelbuchungserviceService,
    private kategorieService: KategorieService) { }

  ngOnInit() {
    this.kategorien = this.kategorieService.getAll();
  }

  private isEinzelbuchungFormOk(): boolean {
    return !this.einzelbuchungMatcher.isErrorState(this.datum, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.name, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.kategorie, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.wert, null);
  }

  hinzufuegen() {
    if (!this.isEinzelbuchungFormOk()) {
      return;
    }

    const neueBuchung: EinzelbuchungAnlegen = {
      name: this.name.value,
      datum: this.datum.value,
      kategorie: this.kategorie.value,
      wert: this.wert.value
    };
    this.datum.reset(new Date());
    this.name.reset();
    this.kategorie.reset(this.kategorien[0]);
    this.wert.reset();
    this.einzelbuchungsService.save(neueBuchung);
  }
}
