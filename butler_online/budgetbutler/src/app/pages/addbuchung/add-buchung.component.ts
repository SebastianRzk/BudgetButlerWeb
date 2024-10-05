import {Component, inject, OnInit} from '@angular/core';
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {EinzelbuchungService} from '../../domain/einzelbuchung.service';
import {Observable} from 'rxjs';
import {Kategorie, KategorieService} from '../../domain/kategorie.service';
import {EinzelbuchungAnlegen, GemeinsameBuchungAnlegen} from '../../domain/model';
import {GemeinsamebuchungService} from '../../domain/gemeinsamebuchung.service';
import {MatButton} from '@angular/material/button';
import {MatCheckbox} from '@angular/material/checkbox';
import {DateAdapter, MatNativeDateModule, MatOption} from '@angular/material/core';
import {AsyncPipe, NgFor} from '@angular/common';
import {MatSelect} from '@angular/material/select';
import {
  MatDatepicker,
  MatDatepickerInput,
  MatDatepickerModule,
  MatDatepickerToggle
} from '@angular/material/datepicker';
import {MatInput} from '@angular/material/input';
import {MatFormField, MatLabel, MatSuffix} from '@angular/material/form-field';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle} from '@angular/material/card';
import {EuropeanNativeDateAdapter} from "../../domain/date-format";
import {BreakpointObserver} from "@angular/cdk/layout";

@Component({
  selector: 'app-addschnelleinstieg',
  templateUrl: './add-buchung.component.html',
  styleUrls: ['./add-buchung.component.css'],
  standalone: true,
  imports: [MatCard,
    MatCardHeader,
    MatCardTitle,
    MatCardContent,
    FormsModule,
    ReactiveFormsModule,
    MatFormField,
    MatLabel,
    MatInput,
    MatDatepickerInput,
    MatDatepickerToggle,
    MatSuffix,
    MatDatepicker,
    MatSelect,
    NgFor,
    MatOption,
    MatCheckbox,
    MatButton,
    AsyncPipe,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  providers: [
    MatDatepickerModule,
    {provide: DateAdapter, useClass: EuropeanNativeDateAdapter}
  ]
})
export class AddBuchungComponent implements OnInit {
  private einzelbuchungsService: EinzelbuchungService = inject(EinzelbuchungService);
  private gemeinsameBuchungenService: GemeinsamebuchungService = inject(GemeinsamebuchungService);
  private kategorieService: KategorieService = inject(KategorieService);

  private breakpointObserver: BreakpointObserver = inject(BreakpointObserver);
  isSmallScreen = this.breakpointObserver.isMatched('(max-width: 799px)');

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
}
