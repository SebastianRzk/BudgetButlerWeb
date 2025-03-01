import { Component, inject, OnInit } from '@angular/core';
import { PartnerInfo, PartnerService } from '../../../domain/partner.service';
import { FormControl, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButton } from '@angular/material/button';
import { MatInput } from '@angular/material/input';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatCard, MatCardContent, MatCardHeader, MatCardTitle } from '@angular/material/card';
import { firstValueFrom } from "rxjs";

@Component({
    selector: 'app-partnername',
    templateUrl: './partnername.component.html',
    styleUrls: ['./partnername.component.css'],
  imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, FormsModule, MatFormField, MatLabel, MatInput, ReactiveFormsModule, MatButton]
})
export class PartnernameComponent implements OnInit {

  private partnerService: PartnerService = inject(PartnerService);

  partnerName = new FormControl('', Validators.required);
  status: string[] = [];
  verknuepfungAktiv = true;

  onClick: () => void = () => {
    if (this.verknuepfungAktiv) {
      firstValueFrom(this.partnerService.deletePartner()).then(() => this.refreshData());
    } else {
      firstValueFrom(this.partnerService.setPartner(this.partnerName.value!)).then(() => this.refreshData());
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
    this.refreshData();
  }

  private refreshData() {
    firstValueFrom(this.partnerService.getPartnerInfo()).then(data => this.setData(data!));
  }
}
