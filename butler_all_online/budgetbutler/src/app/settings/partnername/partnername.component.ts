import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs';
import { PartnerService, PartnerInfo } from '../../partner.service';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-partnername',
  templateUrl: './partnername.component.html',
  styleUrls: ['./partnername.component.css']
})
export class PartnernameComponent implements OnInit {

  partnerName = new FormControl('', Validators.required);
  gebeErweiterteRechte = new FormControl(false);
  status: string[] = [];
  verknuepfungAktiv = true;
  erweiterteRechte = false;

  constructor(private partnerService: PartnerService) {
  }

  onClick: () => void = () => {
    if (this.verknuepfungAktiv) {
      this.partnerService.deletePartner().toPromise().then(data => this.ngOnInit());
    } else {
      this.partnerService.setPartner(this.partnerName.value, this.erweiterteRechte).toPromise().then(data => this.ngOnInit());
    }
  }

  setData: (data: PartnerInfo) => void = (data: PartnerInfo) => {
    this.partnerName.setValue(data.partnername);
    this.status = [];

    if (data.partnername !== '') {
      this.verknuepfungAktiv = true;
      this.partnerName = new FormControl({ value: data.partnername, disabled: true });
      this.gebeErweiterteRechte = new FormControl({value: data.erweiterteRechteGeben, disabled: true});
    } else {
      this.partnerName = new FormControl({ value: '', disabled: false });
      this.gebeErweiterteRechte = new FormControl({value: false, disabled: false});
      this.verknuepfungAktiv = false;
      return;
    }

    if (data.confirmed) {
      this.status.push(`${data.partnername} hat die Verknüpfung bestätigt.`);
    } else {
      this.status.push(`${data.partnername} muss die Verknüpfung noch bestätigen.`);
    }

    if (data.erweiterteRechteBekommen) {
      this.status.push(`${data.partnername} gewährt ihnen erweiterte Rechte.`);
    }

  }

  ngOnInit() {
    this.partnerService.getPartnerInfo().pipe(first()).toPromise().then(data => this.setData(data));
  }

}
