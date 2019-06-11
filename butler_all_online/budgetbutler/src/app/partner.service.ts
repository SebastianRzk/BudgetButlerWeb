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

  constructor(private notificationService: NotificationService, private httpClient: HttpClient, private api: ApiproviderService, private authService: AuthService) { }

  getPartnerInfo: () => Observable<PartnerInfo> = () => {
    if (!this.partnerNameSubject) {
      this.partnerNameSubject = new Subject();
    }
    this.httpClient.get<PartnerInfo>(this.api.getUrl('partner.php')).toPromise().then(data => this.partnerNameSubject.next(data));
    return this.partnerNameSubject.asObservable();
  }

  setPartner: (name: string, erweiterteRechte: boolean) => Observable<Result> = (name: string, erweiterteRechte: boolean) => {
    const partnerInfo: PartnerInfoRequest = {
      partnername: name,
      erweiterteRechteGeben: erweiterteRechte
    };
    return this.httpClient.put<Result>(this.api.getUrl('partner.php'), partnerInfo).pipe(this.logResult);
  }

  deletePartner: () => Observable<Result> = () => {
    return this.httpClient.delete<Result>(this.api.getUrl('partner.php')).pipe(this.logResult);
  }

  private logResult: (data: Observable<Result>) => Observable<Result> = (data: Observable<Result>) => {
    data.subscribe(result => this.notificationService.handleServerResult(result, 'Partner bearbeiten'));
    return data;
  }

  getPartnerNames: () => Promise<string[]> = () => {
    const data = Promise.all(
      [this.authService.getLogin().pipe(first()).toPromise(),
      this.getPartnerInfo().pipe(first()).toPromise()]
    );
    return data.then(
      recData => {
        const authdata: AuthContainer = recData[0];
        const partnerdata: PartnerInfo = recData[1];
        console.log(partnerdata)
        if (partnerdata.partnername && partnerdata.partnername !== '') {
          return [authdata.username, partnerdata.partnername];
        }
        return [authdata.username];
      }
    );
  }
}


export interface PartnerInfo {
  partnername: string;
  confirmed: boolean;
  erweiterteRechteGeben: boolean;
  erweiterteRechteBekommen: boolean;
}

export interface PartnerInfoRequest {
  partnername: string;
  erweiterteRechteGeben: boolean;
}