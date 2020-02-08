import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { EinzelbuchungserviceService } from '../einzelbuchungservice.service';
import { Observable } from 'rxjs';
import { MyErrorStateMatcher } from '../matcher';
import { KategorieService } from '../kategorie.service';
import { EinzelbuchungAnlegen, GemeinsameBuchungAnlegen } from '../model';
import { GemeinsamebuchungService } from '../gemeinsamebuchung.service';
import { AuthService } from '../auth/auth.service';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-addschnelleinstieg',
  templateUrl: './addschnelleinstieg.component.html',
  styleUrls: ['./addschnelleinstieg.component.css']
})
export class AddschnelleinstiegComponent implements OnInit {
  buchungForm = new FormGroup({
    datum: new FormControl(new Date(), Validators.required),
    name: new FormControl('', Validators.required),
    kategorie: new FormControl('', Validators.required),
    wert: new FormControl('', Validators.required),
    gemeinsameBuchung: new FormControl(false)
  });

  kategorien: Observable<string[]>;
  einzelbuchungMatcher = new MyErrorStateMatcher();
  personenName: string;

  constructor(
    private einzelbuchungsService: EinzelbuchungserviceService,
    private gemeinsameBuchungenService: GemeinsamebuchungService,
    private authService: AuthService,
    private kategorieService: KategorieService) { }

  ngOnInit() {
    this.kategorien = this.kategorieService.getAll();
    this.authService.getLogin().pipe(first()).toPromise().then(data => this.personenName = data.username);
  }

  onFormSubmit() {
    if (!this.buchungForm.valid) {
      return;
    }

    if (this.buchungForm.get('gemeinsameBuchung').value) {
      const neueBuchung: GemeinsameBuchungAnlegen = {
        name: this.buchungForm.get('name').value,
        datum: this.buchungForm.get('datum').value,
        kategorie: this.buchungForm.get('kategorie').value,
        wert: this.buchungForm.get('wert').value * -1,
        zielperson: this.personenName
      };
      this.gemeinsameBuchungenService.save(neueBuchung);
    }
    else {
      const neueBuchung: EinzelbuchungAnlegen = {
        name: this.buchungForm.get('name').value,
        datum: this.buchungForm.get('datum').value,
        kategorie: this.buchungForm.get('kategorie').value,
        wert: this.buchungForm.get('wert').value * -1
      };
      this.einzelbuchungsService.save(neueBuchung);
    }
  this.buchungForm.reset({
    datum: new Date(),
    gemeinsameBuchung: this.buchungForm.get('gemeinsameBuchung').value
  });
  }
}
