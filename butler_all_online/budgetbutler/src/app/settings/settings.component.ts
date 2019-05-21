import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { NotEmptyErrorStateMatcher } from '../matcher';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {

  public altesPasswort = new FormControl('', Validators.required);
  public neuesPasswort = new FormControl('', Validators.required);
  public neuesPasswortWiederholung = new FormControl('', Validators.required);

  public passwortMatcher = new NotEmptyErrorStateMatcher();

  public errorMessage = '';

  constructor() { }

  ngOnInit() {
  }

  computeErrorMesage() {
    if (this.altesPasswort.value.length < 8) {
      this.errorMessage = 'Bitte altes Passwort eingeben.';
      return;
    }

    if (this.neuesPasswort.value !== this.neuesPasswortWiederholung.value) {
      this.errorMessage = 'Passwörter sind nicht identisch.';
      return;
    }

    if (this.neuesPasswort.value.length < 8) {
      this.errorMessage = 'Das neue Passwort muss mehr als 8 Zeichen lang sein.';
      return;
    }

    if (this.neuesPasswort.value === this.altesPasswort.value) {
      this.errorMessage = 'Das alte und das neue Passwort dürfen nicht identisch sein.';
      return;
    }

    this.errorMessage = '';
  }

}
