import { Component, inject, OnInit } from '@angular/core';
import { PartnerService, PartnerInfo } from '../../../domain/partner.service';
import {Validators, FormControl} from '@angular/forms';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-partnername',
  templateUrl: './partnername.component.html',
  styleUrls: ['./partnername.component.css']
})
export class PartnernameComponent implements OnInit {

  private partnerService: PartnerService = inject(PartnerService);

  partnerName = new FormControl('', Validators.required);
  status: string[] = [];
  verknuepfungAktiv = true;

  onClick: () => void = () => {
    if (this.verknuepfungAktiv) {
      this.partnerService.deletePartner().toPromise().then(data => this.ngOnInit());
    } else {
      this.partnerService.setPartner(this.partnerName.value).toPromise().then(data => this.ngOnInit());
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
    this.partnerService.getPartnerInfo().pipe(first()).toPromise().then(data => this.setData(data));
  }

}
