import { inject, Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { Result } from './model';
import { HttpClient } from '@angular/common/http';
import { ApiProviderService } from './api-provider.service';

@Injectable({
  providedIn: 'root'
})
export class PartnerService {

  private partnerNameSubject: Subject<PartnerInfo> = new BehaviorSubject<PartnerInfo>({
    bestaetigt: false,
    zielperson: ''
  });

  private httpClient: HttpClient = inject(HttpClient);
  private api: ApiProviderService = inject(ApiProviderService);

  getPartnerInfo: () => Observable<PartnerInfo> = () => {
    this.httpClient.get<PartnerInfo>(this.api.getUrl('partnerstatus')).subscribe(data => this.partnerNameSubject.next(data));
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
