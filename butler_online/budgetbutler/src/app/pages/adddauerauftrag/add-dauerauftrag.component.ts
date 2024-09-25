import { Component, inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators, FormsModule, ReactiveFormsModule } from "@angular/forms";
import {Observable} from "rxjs";
import { Kategorie, KategorieService } from "../../domain/kategorie.service";
import {
  DauerauftragAnlegen,
  GemeinsamerDauerauftragAnlegen
} from "../../domain/model";
import {DauerauftraegeService} from "../../domain/dauerauftraege.service";
import {GemeinsameDauerauftraegeService} from "../../domain/gemeinsame-dauerauftraege.service";
import { MatButton } from '@angular/material/button';
import { MatCheckbox } from '@angular/material/checkbox';
import {MatNativeDateModule, MatOption} from '@angular/material/core';
import { NgFor, AsyncPipe } from '@angular/common';
import { MatSelect } from '@angular/material/select';
import {
  MatDatepickerInput,
  MatDatepickerToggle,
  MatDatepicker,
  MatDatepickerModule
} from '@angular/material/datepicker';
import { MatInput } from '@angular/material/input';
import { MatFormField, MatLabel, MatSuffix } from '@angular/material/form-field';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';

@Component({
    selector: 'app-adddauerauftrag',
    templateUrl: './add-dauerauftrag.component.html',
    styleUrls: ['./add-dauerauftrag.component.css'],
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
    MatNativeDateModule
  ]
})
export class AddDauerauftragComponent implements OnInit {
  buchungForm = new FormGroup({
    startDatum: new FormControl(new Date(), Validators.required),
    endeDatum: new FormControl(null, Validators.required),
    name: new FormControl('', Validators.required),
    kategorie: new FormControl('', Validators.required),
    wert: new FormControl<number>(0, Validators.required),
    rhythmus: new FormControl<string>('monatlich', Validators.required),
    gemeinsameBuchung: new FormControl(false)
  });

  private kategorieService: KategorieService = inject(KategorieService);
  private dauerauftragService: DauerauftraegeService = inject(DauerauftraegeService);
  private gemeinsamerDauerauftragService: GemeinsameDauerauftraegeService = inject(GemeinsameDauerauftraegeService)

  kategorien: Observable<Kategorie[]> = this.kategorieService.kategorien$;

  rhythmus = [
    {
      value: 'monatlich',
      displayName: 'monatlich'
    },
    {
      value: 'viertel_jaehrlich',
      displayName: 'vierteljährlich'
    },
    {
      value: 'halb_jaehrlich',
      displayName: 'halbjährlich'
    },
    {
      value: 'jaehrlich',
      displayName: 'jährlich'
    }
  ];


  ngOnInit() {
    this.kategorieService.refresh();
  }

  onFormSubmit() {
    if (!this.buchungForm.valid) {
      return;
    }

    if (this.buchungForm.get('gemeinsameBuchung')!.value) {
      const neuerDauerauftrag: GemeinsamerDauerauftragAnlegen = {
        name: this.buchungForm.get('name')!.value!,
        startDatum: this.buchungForm.get('startDatum')!.value!,
        endeDatum: this.buchungForm.get('endeDatum')!.value!,
        kategorie: this.buchungForm.get('kategorie')!.value!,
        rhythmus: this.buchungForm.get('rhythmus')!.value!,
        wert: this.buchungForm.get('wert')!.value! * -1,
        eigeneBuchung: true
      };
      this.gemeinsamerDauerauftragService.save(neuerDauerauftrag);
    } else {
      const neuerDauerauftrag: DauerauftragAnlegen = {
        name: this.buchungForm.get('name')!.value!,
        startDatum: this.buchungForm.get('startDatum')!.value!,
        endeDatum: this.buchungForm.get('endeDatum')!.value!,
        kategorie: this.buchungForm.get('kategorie')!.value!,
        rhythmus: this.buchungForm.get('rhythmus')!.value!,
        wert: this.buchungForm.get('wert')!.value! * -1
      };
      this.dauerauftragService.save(neuerDauerauftrag);
    }
    this.buchungForm.reset(
      {
        startDatum: new Date(),
        gemeinsameBuchung: this.buchungForm.get('gemeinsameBuchung')!.value
      });
  }

}
