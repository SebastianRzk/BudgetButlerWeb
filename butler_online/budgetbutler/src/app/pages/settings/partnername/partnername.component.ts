import { Component, inject, OnInit } from '@angular/core';
import { PartnerService, PartnerInfo } from '../../../domain/partner.service';
import { Validators, FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { first } from 'rxjs/operators';
import { MatButton } from '@angular/material/button';
import { NgFor, NgIf } from '@angular/common';
import { MatInput } from '@angular/material/input';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';
import {firstValueFrom} from "rxjs";

@Component({
    selector: 'app-partnername',
    templateUrl: './partnername.component.html',
    styleUrls: ['./partnername.component.css'],
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, FormsModule, MatFormField, MatLabel, MatInput, ReactiveFormsModule, NgFor, NgIf, MatButton]
})
export class PartnernameComponent implements OnInit {

  private partnerService: PartnerService = inject(PartnerService);

  partnerName = new FormControl('', Validators.required);
  status: string[] = [];
  verknuepfungAktiv = true;

  onClick: () => void = () => {
    if (this.verknuepfungAktiv) {
      firstValueFrom(this.partnerService.deletePartner()).then(() => this.ngOnInit());
    } else {
      firstValueFrom(this.partnerService.setPartner(this.partnerName.value!)).then(() => this.ngOnInit());
    }
  }

  setData: (data: PartnerInfo) => void = (data: PartnerInfo) => {
    this.partnerName.setValue(data.zielperson);
    this.status = [];

    if (data.zielperson !== '') {
      this.verknuepfungAktiv = true;
      this.partnerName.disable();
    } else {
      this.partnerName.enable();
      this.verknuepfungAktiv = false;
      return;
    }

    if (data.bestaetigt) {
      this.status.push(`${data.zielperson} hat die Verknüpfung bestätigt.`);
    } else {
      this.status.push(`${data.zielperson} muss die Verknüpfung noch bestätigen.`);
    }
  }

  ngOnInit() {
    this.partnerService.getPartnerInfo().pipe(first()).toPromise().then(data => this.setData(data!));
  }

}
