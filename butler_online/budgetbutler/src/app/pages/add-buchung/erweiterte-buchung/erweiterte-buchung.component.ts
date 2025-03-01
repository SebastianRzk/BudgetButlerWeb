import { Component, EventEmitter, inject, Input, OnInit, Output } from '@angular/core';
import { MatCardModule } from "@angular/material/card";
import { BehaviorSubject, firstValueFrom, Observable, Subject } from "rxjs";
import { AsyncPipe, DatePipe, DecimalPipe, JsonPipe } from "@angular/common";
import { FormArray, FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatCheckboxModule } from "@angular/material/checkbox";
import { MatInputModule } from "@angular/material/input";
import { MatSelectModule } from "@angular/material/select";
import { KategorieService } from "../../../domain/kategorie.service";
import { MatButton } from "@angular/material/button";

@Component({
  selector: 'app-erweiterte-buchung',
  imports: [
    MatCardModule,
    AsyncPipe,
    DecimalPipe,
    DatePipe,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatCheckboxModule,
    MatInputModule,
    MatSelectModule,
    JsonPipe,
    MatButton,
  ],
  templateUrl: './erweiterte-buchung.component.html',
  styleUrl: './erweiterte-buchung.component.css'
})
export class ErweiterteBuchungComponent implements OnInit {

  @Input({required: true})
  public gemeinsam!: boolean;

  @Input({required: true})
  public name!: string;

  @Input({required: true})
  public datum!: Date;

  @Input({required: true})
  public kategorie!: string;

  @Input({required: true})
  public gesamtBetrag!: number;

  @Output()
  public submitEvent: EventEmitter<BuchungEvent[]> = new EventEmitter<BuchungEvent[]>();

  private restBetrag: Subject<number> = new BehaviorSubject<number>(0);
  public restBetrag$: Observable<number> = this.restBetrag.asObservable();

  private kategorieService: KategorieService = inject(KategorieService);
  kategorien = this.kategorieService.kategorien$;

  private status = new BehaviorSubject({
    notOk: false,
    message: ''
  });
  public status$: Observable<Status> = this.status.asObservable();


  formBuilder = inject(FormBuilder);
  form: FormGroup<{
    buchungen: FormArray
  }> = this.formBuilder.group({
    buchungen: this.formBuilder.array([])
  });


  ngOnInit(): void {
    this.restBetrag.next(this.gesamtBetrag);
    for (let i = 0; i < 3; i++) {
      const group = this.formBuilder.group({
        name: new FormControl<string>('', Validators.required),
        betrag: new FormControl<number>(0, Validators.required),
        kategorie: new FormControl<string>('', Validators.required),
        gemeinsam: new FormControl<boolean>(false)
      });
      if (i != 0) {
        group.disable()
      }

      this.form.controls['buchungen'].push(
        group
      );
    }
  }

  recalcGesamtsumme(): void {
    let betrag = this.gesamtBetrag;
    let betragZero = false;
    for (let i = 0; i < this.form.controls.buchungen.length; i++) {
      if (this.form.controls.buchungen.at(i).disabled) {
        continue
      }
      const controlBetrag = this.form.controls.buchungen.at(i).value.betrag;
      betrag -= controlBetrag;
      if (controlBetrag == 0) {
        betragZero = true;
      }
    }
    if (betrag <= 0) {
      this.status.next({
        notOk: true,
        message: 'Die Summe der Buchungen darf nicht größer als oder gleich dem Gesamtbetrag sein'
      });
      return;
    }
    if (betragZero) {
      this.status.next({
        notOk: true,
        message: 'Einzelne Buchungen dürfen nicht 0 sein'
      });
      return;
    }

    this.status.next({
      notOk: false,
      message: ''
    });
    this.restBetrag.next(betrag);
  }

  disable(index: number, active: boolean): void {
    if (active) {
      this.form.controls['buchungen'].at(index).enable();
    }else {
      this.form.controls['buchungen'].at(index).disable();
    }
    this.recalcGesamtsumme();
  }

  async submit() {
    const restbetrag = await firstValueFrom(this.restBetrag$);
    const values = [
      {
        datum: this.datum,
        name: this.name,
        betrag: restbetrag,
        kategorie: this.kategorie,
        gemeinsam: this.gemeinsam
      }
    ];
    for (const element of this.form.controls['buchungen'].value) {
      if (element.name.disabled) {
        continue
      }
      values.push({
        datum: this.datum,
        name: element.name,
        betrag: element.betrag,
        kategorie: element.kategorie,
        gemeinsam: element.gemeinsam
      });
    }
    console.log(values);
    this.submitEvent.next(values)
  }
}

interface Status {
  notOk: boolean,
  message: string
}

export interface BuchungEvent {
  datum: Date,
  name: string,
  betrag: number,
  kategorie: string,
  gemeinsam: boolean
}
