import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { NotEmptyErrorStateMatcher } from '../matcher';
import { AuthService } from '../auth/auth.service';
import { ALTES_PASSWORT_FEHLT, PASSWOERTER_NICHT_GLEICH, PASSWORT_ZU_KURZ, PASSWORT_IDENTISCH } from '../errormessages';

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

  constructor(private authService: AuthService) { }

  ngOnInit() {
  }

  computeErrorMesage() {
    if (this.altesPasswort.value.length < 8) {
      this.errorMessage = ALTES_PASSWORT_FEHLT;
      return;
    }

    if (this.neuesPasswort.value !== this.neuesPasswortWiederholung.value) {
      this.errorMessage = PASSWOERTER_NICHT_GLEICH;
      return;
    }

    if (this.neuesPasswort.value.length < 8) {
      this.errorMessage = PASSWORT_ZU_KURZ;
      return;
    }

    if (this.neuesPasswort.value === this.altesPasswort.value) {
      this.errorMessage = PASSWORT_IDENTISCH;
      return;
    }

    this.errorMessage = '';
  }


  changePassword() {
    this.computeErrorMesage();

    if (this.errorMessage !== '') {
      return;
    }

    this.authService.changePassword(this.altesPasswort.value, this.neuesPasswort.value);
    this.altesPasswort.setValue('');
    this.neuesPasswort.setValue('');
    this.neuesPasswortWiederholung.setValue('');
  }


}
