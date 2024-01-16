import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { Result } from './model';
import { HttpClient } from '@angular/common/http';
import { ApiproviderService } from './apiprovider.service';

@Injectable({
  providedIn: 'root'
})
export class PartnerService {

  private partnerNameSubject: Subject<PartnerInfo>;

  constructor(private httpClient: HttpClient,
              private api: ApiproviderService) { }

  getPartnerInfo: () => Observable<PartnerInfo> = () => {
    if (!this.partnerNameSubject) {
      this.partnerNameSubject = new Subject();
    }
    this.httpClient.get<PartnerInfo>(this.api.getUrl('partnerstatus')).toPromise().then(data => this.partnerNameSubject.next(data));
    return this.partnerNameSubject.asObservable();
  }

  setPartner: (name: string) => Observable<Result> = (name: string) => {
    const partnerInfo: PartnerInfoDto = {
      zielperson: name
    };
    return this.httpClient.post<Result>(this.api.getUrl('partnerstatus'), partnerInfo);
  }

  deletePartner: () => Observable<Result> = () => {
    return this.httpClient.delete<Result>(this.api.getUrl('partnerstatus'));
  }
}


export interface PartnerInfo {
  zielperson: string;
  bestaetigt: boolean;
}

export interface PartnerInfoDto {
  zielperson: string;
}
