import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {EinzelbuchungService} from '../../domain/einzelbuchung.service';
import {Observable} from 'rxjs';
import {KategorieService} from '../../domain/kategorie.service';
import {EinzelbuchungAnlegen, GemeinsameBuchungAnlegen} from '../../domain/model';
import {GemeinsamebuchungService} from '../../domain/gemeinsamebuchung.service';
import {AuthService} from '../auth/auth.service';
import {first} from 'rxjs/operators';

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
    wert: new FormControl<number>(null, Validators.required),
    gemeinsameBuchung: new FormControl(false)
  });

  kategorien: Observable<string[]>;

  constructor(
    private einzelbuchungsService: EinzelbuchungService,
    private gemeinsameBuchungenService: GemeinsamebuchungService,
    private authService: AuthService,
    private kategorieService: KategorieService) {
  }

  ngOnInit() {
    this.kategorien = this.kategorieService.getAll();
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
        eigeneBuchung: true
      };
      this.gemeinsameBuchungenService.save(neueBuchung);
    } else {
      const neueBuchung: EinzelbuchungAnlegen = {
        name: this.buchungForm.get('name').value,
        datum: this.buchungForm.get('datum').value,
        kategorie: this.buchungForm.get('kategorie').value,
        wert: this.buchungForm.get('wert').value * -1
      };
      this.einzelbuchungsService.save(neueBuchung);
    }
    this.buchungForm.reset(
      {
        datum: new Date(),
        gemeinsameBuchung: this.buchungForm.get('gemeinsameBuchung').value
      });
  }
}
