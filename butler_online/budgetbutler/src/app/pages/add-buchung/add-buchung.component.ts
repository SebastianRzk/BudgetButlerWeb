import {Component, inject, OnInit} from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {EinzelbuchungService} from '../../domain/einzelbuchung.service';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
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
import { BuchungEvent, ErweiterteBuchungComponent } from "./erweiterte-buchung/erweiterte-buchung.component";

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
    CommonModule,
    ErweiterteBuchungComponent
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

  private istErweiterteBuchung: Subject<boolean> = new BehaviorSubject(false);
  public istErweiterteBuchung$: Observable<boolean> = this.istErweiterteBuchung.asObservable();

  buchungForm = new FormGroup({
    datum: new FormControl(new Date(), Validators.required),
    name: new FormControl('', Validators.required),
    kategorie: new FormControl('', Validators.required),
    wert: new FormControl<number>(0, Validators.required),
    gemeinsameBuchung: new FormControl(false)
  });

  kategorien: Observable<Kategorie[]> = this.kategorieService.kategorien$;


  ngOnInit() {
    this.istErweiterteBuchung.next(false);
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

    const isGemeinsam = this.buchungForm.get('gemeinsameBuchung')!.value;
    const name = this.buchungForm.get('name')!.value!;
    const datum = this.buchungForm.get('datum')!.value!;
    const kategorie = this.buchungForm.get('kategorie')!.value!;
    const rawValue = this.buchungForm.get('wert')!.value!;
    this.saveBuchung(isGemeinsam!, name, datum, kategorie, rawValue);
    this.resetForm();
  }


  private saveBuchung(isGemeinsam: boolean, name: string, datum: Date, kategorie: string, rawValue: number) {
    if (isGemeinsam) {
      const neueBuchung: GemeinsameBuchungAnlegen = {
        name: name,
        datum: datum,
        kategorie: kategorie,
        wert: rawValue * -1,
        eigeneBuchung: true
      };
      this.gemeinsameBuchungenService.save(neueBuchung);
    } else {
      const neueBuchung: EinzelbuchungAnlegen = {
        name: name,
        datum: datum,
        kategorie: kategorie,
        wert: rawValue * -1
      };
      this.einzelbuchungsService.save(neueBuchung);
    }
  }

  private resetForm() {
    this.buchungForm.reset(
      {
        datum: new Date(),
        gemeinsameBuchung: this.buchungForm.get('gemeinsameBuchung')!.value
      });
    this.buchungForm.markAsUntouched();
    this.istErweiterteBuchung.next(false)
  }

  onConsumeSubBuchung(buchungen: BuchungEvent[]){
    for (const buchung of buchungen) {
      this.saveBuchung(buchung.gemeinsam, buchung.name, buchung.datum, buchung.kategorie, buchung.betrag);
    }
    this.resetForm();
  }

  onTeilenClick(){
    if (!this.buchungForm.valid) {
      return;
    }
    this.istErweiterteBuchung.next(true);
  }
}
