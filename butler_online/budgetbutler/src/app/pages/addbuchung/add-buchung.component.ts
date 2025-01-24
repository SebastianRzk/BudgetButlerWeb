import {Component, inject, OnInit} from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {EinzelbuchungService} from '../../domain/einzelbuchung.service';
import {Observable} from 'rxjs';
import {Kategorie, KategorieService} from '../../domain/kategorie.service';
import {EinzelbuchungAnlegen, GemeinsameBuchungAnlegen} from '../../domain/model';
import {GemeinsamebuchungService} from '../../domain/gemeinsamebuchung.service';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MAT_DATE_LOCALE, provideNativeDateAdapter} from '@angular/material/core';
import {AsyncPipe, CommonModule} from '@angular/common';
import {MatSelectModule} from '@angular/material/select';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatCardModule} from '@angular/material/card';
import {BreakpointObserver} from "@angular/cdk/layout";

@Component({
  selector: 'app-addschnelleinstieg',
  templateUrl: './add-buchung.component.html',
  styleUrls: ['./add-buchung.component.css'],
  imports: [
    MatCardModule,
    MatFormFieldModule,
    MatDatepickerModule,
    AsyncPipe,
    MatSelectModule,
    MatCheckboxModule,
    MatInputModule,
    ReactiveFormsModule,
    MatButtonModule,
    CommonModule
  ],
  providers: [
    provideNativeDateAdapter(),
    {
      provide: MAT_DATE_LOCALE,
      useValue: 'de-DE'
    }
  ],
})
export class AddBuchungComponent implements OnInit {
  private einzelbuchungsService: EinzelbuchungService = inject(EinzelbuchungService);
  private gemeinsameBuchungenService: GemeinsamebuchungService = inject(GemeinsamebuchungService);
  private kategorieService: KategorieService = inject(KategorieService);

  isSmallScreen = inject(BreakpointObserver).isMatched('(max-width: 799px)');

  buchungForm = new FormGroup({
    datum: new FormControl(new Date(), Validators.required),
    name: new FormControl('', Validators.required),
    kategorie: new FormControl('', Validators.required),
    wert: new FormControl<number>(0, Validators.required),
    gemeinsameBuchung: new FormControl(false)
  });

  kategorien: Observable<Kategorie[]> = this.kategorieService.kategorien$;


  ngOnInit() {
    this.kategorieService.refresh();
    this.buchungForm.reset(
      {
        datum: new Date(),
      }
    );
    this.buchungForm.markAsUntouched();
  }

  onFormSubmit() {
    if (!this.buchungForm.valid) {
      return;
    }

    if (this.buchungForm.get('gemeinsameBuchung')!.value) {
      const neueBuchung: GemeinsameBuchungAnlegen = {
        name: this.buchungForm.get('name')!.value!,
        datum: this.buchungForm.get('datum')!.value!,
        kategorie: this.buchungForm.get('kategorie')!.value!,
        wert: this.buchungForm.get('wert')!.value! * -1,
        eigeneBuchung: true
      };
      this.gemeinsameBuchungenService.save(neueBuchung);
    } else {
      const neueBuchung: EinzelbuchungAnlegen = {
        name: this.buchungForm.get('name')!.value!,
        datum: this.buchungForm.get('datum')!.value!,
        kategorie: this.buchungForm.get('kategorie')!.value!,
        wert: this.buchungForm.get('wert')!.value! * -1
      };
      this.einzelbuchungsService.save(neueBuchung);
    }
    this.buchungForm.reset(
      {
        datum: new Date(),
        gemeinsameBuchung: this.buchungForm.get('gemeinsameBuchung')!.value
      });
    this.buchungForm.markAsUntouched();
  }

  protected readonly console = console;
}
