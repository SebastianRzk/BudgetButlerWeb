import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { EinzelbuchungserviceService } from '../einzelbuchungservice.service';
import { Observable } from 'rxjs';
import { MyErrorStateMatcher } from '../matcher';
import { KategorieService } from '../kategorie.service';
import { EinzelbuchungAnlegen, GemeinsameBuchung, GemeinsameBuchungAnlegen } from '../model';
import { GemeinsamebuchungService } from '../gemeinsamebuchung.service';
import { AuthService, AuthContainer } from '../auth/auth.service';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-addschnelleinstieg',
  templateUrl: './addschnelleinstieg.component.html',
  styleUrls: ['./addschnelleinstieg.component.css']
})
export class AddschnelleinstiegComponent implements OnInit {

  datum = new FormControl(new Date(), Validators.required);
  name = new FormControl('', Validators.required);
  kategorie = new FormControl('', Validators.required);
  wert = new FormControl('', Validators.required);
  gemeinsameBuchung = new FormControl(false);

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

  private isEinzelbuchungFormOk(): boolean {
    return this.datum.valid &&
      this.name.valid &&
      this.kategorie.valid &&
      this.wert.valid
  }

  hinzufuegen() {
    if (!this.isEinzelbuchungFormOk()) {
      return;
    }

    if (this.gemeinsameBuchung.value) {
      const neueBuchung: GemeinsameBuchungAnlegen = {
        name: this.name.value,
        datum: this.datum.value,
        kategorie: this.kategorie.value,
        wert: this.wert.value * -1,
        zielperson: this.personenName
      };
      this.gemeinsameBuchungenService.save(neueBuchung);

    } else {
      const neueBuchung: EinzelbuchungAnlegen = {
        name: this.name.value,
        datum: this.datum.value,
        kategorie: this.kategorie.value,
        wert: this.wert.value * -1
      };
      this.einzelbuchungsService.save(neueBuchung);
    }
    this.datum.reset(new Date());
    this.name.reset();
    this.kategorie.reset(this.kategorien[0]);
    this.wert.reset();
  }
}
