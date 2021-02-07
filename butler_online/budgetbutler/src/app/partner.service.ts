import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { Result } from './model';
import { NotificationService } from './notification.service';
import { HttpClient } from '@angular/common/http';
import { ApiproviderService } from './apiprovider.service';
import { AuthService, AuthContainer } from './auth/auth.service';
import { first } from 'rxjs/operators';

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
    this.httpClient.get<PartnerInfo>(this.api.getUrl('partner.php')).toPromise().then(data => this.partnerNameSubject.next(data));
    return this.partnerNameSubject.asObservable();
  }

  setPartner: (name: string) => Observable<Result> = (name: string) => {
    const partnerInfo: PartnerInfoRequest = {
      partnername: name
    };
    return this.httpClient.put<Result>(this.api.getUrl('partner.php'), partnerInfo);
  }

  deletePartner: () => Observable<Result> = () => {
    return this.httpClient.delete<Result>(this.api.getUrl('partner.php'));
  }
}


export interface PartnerInfo {
  partnername: string;
  confirmed: boolean;
}

export interface PartnerInfoRequest {
  partnername: string;
}
