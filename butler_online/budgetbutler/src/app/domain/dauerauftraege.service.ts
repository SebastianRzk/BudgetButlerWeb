import {inject, Injectable} from '@angular/core';
import { HttpClient } from "@angular/common/http";
import {ApiProviderService} from "./api-provider.service";
import {
  Dauerauftrag,
  DauerauftragAnlegen, DauerauftragLoeschen, ERROR_LOADING_DAUERAUFTRAEGE,
  ERROR_RESULT,
  Result
} from "./model";
import {DauerauftragAnlegenTO, DauerauftragTO} from "./modelTo";
import {toDauerauftrag, toDauerauftragAnlegenTO} from "./mapper";
import {NotificationService} from "./notification.service";
import {BehaviorSubject} from "rxjs";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class DauerauftraegeService {

  private httpClient: HttpClient = inject(HttpClient);

  private apiProvider: ApiProviderService = inject(ApiProviderService);

  private notification: NotificationService = inject(NotificationService);

  private dauerauftrage = new BehaviorSubject<Dauerauftrag[]>([]);
  public readonly dauerauftraege$ = this.dauerauftrage.asObservable();


  save(anlegen: DauerauftragAnlegen){
    const dto: DauerauftragAnlegenTO = toDauerauftragAnlegenTO(anlegen);
    this.httpClient.post<Result>(this.apiProvider.getUrl('dauerauftrag'), dto).subscribe(
      data => this.notification.handleServerResult(data, 'Speichern des Dauerauftrags'),
      error => this.notification.handleError(error, ERROR_RESULT, 'Speichern des Dauerauftrags')
    );
  }

  public refresh(): void {
    this.httpClient.get<DauerauftragTO[]>(this.apiProvider.getUrl('dauerauftraege')).pipe(map( x => x.map(toDauerauftrag))).subscribe(
      x => this.dauerauftrage.next(x),
      error => this.notification.handleError(error, ERROR_LOADING_DAUERAUFTRAEGE, ERROR_LOADING_DAUERAUFTRAEGE.message));
  }

  public delete(dauerauftragLoeschen: DauerauftragLoeschen) {
    this.httpClient.delete<Result>(this.apiProvider.getUrl('dauerauftrag/' + dauerauftragLoeschen.id)).subscribe(
      data => {
        this.notification.handleServerResult(data, 'Löschen der Ausgabe');
        this.refresh();
      },
      error => {
        this.notification.handleError(error, ERROR_RESULT, 'Löschen der Ausgabe');
        this.refresh();
      }
    );
  }

}

