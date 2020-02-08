import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { AuthService } from '../auth/auth.service';
import { ALTES_PASSWORT_FEHLT, PASSWOERTER_NICHT_GLEICH, PASSWORT_IDENTISCH, PASSWORT_ZU_KURZ } from './errormessages';
import { MyErrorStateMatcher } from '../matcher';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {

  neuesPasswortForm = new FormGroup({
    altesPasswort: new FormControl('', Validators.required),
    neuesPasswort: new FormControl('', Validators.required),
    neuesPasswortWiederholung: new FormControl('', Validators.required)
  });

  public errorMessage = '';

  constructor(private authService: AuthService) { }

  ngOnInit() {
  }

  computeErrorMesage() {
    if (this.neuesPasswortForm.get('altesPasswort').value.length < 8) {
      this.errorMessage = ALTES_PASSWORT_FEHLT;
      return;
    }

    if (this.neuesPasswortForm.get('neuesPasswort').value !== this.neuesPasswortForm.get('neuesPasswortWiederholung').value) {
      this.errorMessage = PASSWOERTER_NICHT_GLEICH;
      return;
    }

    if (this.neuesPasswortForm.get('neuesPasswort').value.length < 8) {
      this.errorMessage = PASSWORT_ZU_KURZ;
      return;
    }

    if (this.neuesPasswortForm.get('neuesPasswort').value === this.neuesPasswortForm.get('altesPasswort').value) {
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

    this.authService.changePassword(this.neuesPasswortForm.get('altesPasswort').value, this.neuesPasswortForm.get('neuesPasswort').value);
    this.neuesPasswortForm.reset();
  }


}
