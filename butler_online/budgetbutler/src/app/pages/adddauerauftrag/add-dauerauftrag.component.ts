import { Component, inject, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {Observable} from "rxjs";
import { Kategorie, KategorieService } from "../../domain/kategorie.service";
import {
  DauerauftragAnlegen,
  GemeinsamerDauerauftragAnlegen
} from "../../domain/model";
import {DauerauftraegeService} from "../../domain/dauerauftraege.service";
import {GemeinsameDauerauftraegeService} from "../../domain/gemeinsame-dauerauftraege.service";

@Component({
  selector: 'app-adddauerauftrag',
  templateUrl: './add-dauerauftrag.component.html',
  styleUrls: ['./add-dauerauftrag.component.css']
})
export class AddDauerauftragComponent implements OnInit {
  buchungForm = new FormGroup({
    startDatum: new FormControl(new Date(), Validators.required),
    endeDatum: new FormControl(null, Validators.required),
    name: new FormControl('', Validators.required),
    kategorie: new FormControl('', Validators.required),
    wert: new FormControl<number>(null, Validators.required),
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

    if (this.buchungForm.get('gemeinsameBuchung').value) {
      const neuerDauerauftrag: GemeinsamerDauerauftragAnlegen = {
        name: this.buchungForm.get('name').value,
        startDatum: this.buchungForm.get('startDatum').value,
        endeDatum: this.buchungForm.get('endeDatum').value,
        kategorie: this.buchungForm.get('kategorie').value,
        rhythmus: this.buchungForm.get('rhythmus').value,
        wert: this.buchungForm.get('wert').value * -1,
        eigeneBuchung: true
      };
      this.gemeinsamerDauerauftragService.save(neuerDauerauftrag);
    } else {
      const neuerDauerauftrag: DauerauftragAnlegen = {
        name: this.buchungForm.get('name').value,
        startDatum: this.buchungForm.get('startDatum').value,
        endeDatum: this.buchungForm.get('endeDatum').value,
        kategorie: this.buchungForm.get('kategorie').value,
        rhythmus: this.buchungForm.get('rhythmus').value,
        wert: this.buchungForm.get('wert').value * -1
      };
      this.dauerauftragService.save(neuerDauerauftrag);
    }
    this.buchungForm.reset(
      {
        startDatum: new Date(),
        gemeinsameBuchung: this.buchungForm.get('gemeinsameBuchung').value
      });
  }

}
