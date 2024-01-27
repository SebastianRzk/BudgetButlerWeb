import { Component, inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { EinzelbuchungService } from '../../domain/einzelbuchung.service';
import { Observable } from 'rxjs';
import { Kategorie, KategorieService } from '../../domain/kategorie.service';
import { EinzelbuchungAnlegen, GemeinsameBuchungAnlegen } from '../../domain/model';
import { GemeinsamebuchungService } from '../../domain/gemeinsamebuchung.service';

@Component({
  selector: 'app-addschnelleinstieg',
  templateUrl: './add-buchung.component.html',
  styleUrls: ['./add-buchung.component.css']
})
export class AddBuchungComponent implements OnInit {
  private einzelbuchungsService: EinzelbuchungService = inject(EinzelbuchungService);
  private gemeinsameBuchungenService: GemeinsamebuchungService = inject(GemeinsamebuchungService);
  private kategorieService: KategorieService = inject(KategorieService);


  buchungForm = new FormGroup({
    datum: new FormControl(new Date(), Validators.required),
    name: new FormControl('', Validators.required),
    kategorie: new FormControl('', Validators.required),
    wert: new FormControl<number>(null, Validators.required),
    gemeinsameBuchung: new FormControl(false)
  });

  kategorien: Observable<Kategorie[]> = this.kategorieService.kategorien$;


  ngOnInit() {
    this.kategorieService.refresh();
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
