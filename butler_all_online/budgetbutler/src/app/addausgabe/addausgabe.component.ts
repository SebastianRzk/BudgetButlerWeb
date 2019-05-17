import { Component, OnInit } from '@angular/core';
import { Einzelbuchung } from '../model';
import { EinzelbuchungserviceService } from '../einzelbuchungservice.service';
import { NotificationService } from '../notification.service';
import { FormControl, FormGroupDirective, NgForm, Validators, NgControlStatus, AbstractControl, FormBuilder } from '@angular/forms';
import { toEinzelbuchungTO } from '../converter';
import { ErrorStateMatcher } from '@angular/material';
import { KategorieService } from '../kategorie.service';
import { AbstractControlStatus } from '@angular/forms/src/directives/ng_control_status';

export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return (!!(control && control.invalid && (control.dirty || control.touched || isSubmitted))) || (control.value === '');
  }
}


@Component({
  selector: 'app-addausgabe',
  templateUrl: './addausgabe.component.html',
  styleUrls: ['./addausgabe.component.css']
})
export class AddausgabeComponent implements OnInit {

  datum = new FormControl(new Date(), Validators.required);
  name = new FormControl('', Validators.required);
  kategorie = new FormControl('', Validators.required);
  kategorien: string[] = [];
  wert = new FormControl('', Validators.required);
  einzelbuchungMatcher = new MyErrorStateMatcher();


  neueKategorieMatcher = new MyErrorStateMatcher();
  neueKategorie = new FormControl('', Validators.required);


  constructor(
    private einzelbuchungsService: EinzelbuchungserviceService,
    private kategorieService: KategorieService) { }

  ngOnInit() {
    this.kategorieService.getAll().subscribe(data => {
      this.kategorien = data;
      if (data.length > 0) {
        this.kategorie.setValue(data[0]);
      }
    });
  }

  private isEinzelbuchungFormOk(): boolean {
    return !this.einzelbuchungMatcher.isErrorState(this.datum, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.name, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.kategorie, null) &&
      !this.einzelbuchungMatcher.isErrorState(this.wert, null);
  }

  hinzufuegen() {
    if (! this.isEinzelbuchungFormOk()) {
      return;
    }

    const neueBuchung: Einzelbuchung = {
      id: 0,
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

  setKategorie() {
    if (this.neueKategorie.value === '') {
      return;
    }
    const value: string = this.neueKategorie.value;
    this.kategorien.push(value);
    this.neueKategorie.reset();
    this.kategorie.setValue(value);
  }

}
