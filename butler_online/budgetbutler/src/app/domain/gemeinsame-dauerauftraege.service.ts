import { inject, Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { ApiProviderService } from "./api-provider.service";
import { NotificationService } from "./notification.service";
import {
  DauerauftragLoeschen,
  ERROR_LOADING_GEMEINSME_DAUERAUFTRAEGE,
  ERROR_RESULT,
  GemeinsamerDauerauftrag,
  GemeinsamerDauerauftragAnlegen,
  Result
} from "./model";
import { GemeinsamerDauerauftragAnlegenTO, GemeinsamerDauerauftragTO } from "./modelTo";
import { toGemeinsamerDauerauftrag, toGemeinsamerDauerauftragAnlegenTO } from "./mapper";
import { BehaviorSubject } from "rxjs";
import { map } from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class GemeinsameDauerauftraegeService {
  private httpClient: HttpClient = inject(HttpClient);

  private apiProvider: ApiProviderService = inject(ApiProviderService);

  private notification: NotificationService = inject(NotificationService);


  private gemeinsameDauerauftraege = new BehaviorSubject<GemeinsamerDauerauftrag[]>([]);
  public readonly gemeinsameDauerauftrage$ = this.gemeinsameDauerauftraege.asObservable();


  save(anlegen: GemeinsamerDauerauftragAnlegen) {
    const dto: GemeinsamerDauerauftragAnlegenTO = toGemeinsamerDauerauftragAnlegenTO(anlegen);
    this.httpClient.post<Result>(this.apiProvider.getUrl('gemeinsamer_dauerauftrag'), dto).subscribe(
      data => this.notification.handleServerResult(data, 'Speichern des gemeinsamen Dauerauftrags'),
      error => this.notification.handleError(error, ERROR_RESULT, 'Speichern des gemeinsamen Dauerauftrags')
    );
  }


  public refresh(): void {
    this.httpClient.get<GemeinsamerDauerauftragTO[]>(this.apiProvider.getUrl('gemeinsame_dauerauftraege'))
      .pipe(map(x => x.map(toGemeinsamerDauerauftrag))).subscribe(
      x => this.gemeinsameDauerauftraege.next(x),
      error => this.notification.handleError(error,
        ERROR_LOADING_GEMEINSME_DAUERAUFTRAEGE, ERROR_LOADING_GEMEINSME_DAUERAUFTRAEGE.message));
  }

  public delete(dauerauftragLoeschen: DauerauftragLoeschen) {
    this.httpClient.delete<Result>(this.apiProvider.getUrl('gemeinsamer_dauerauftrag/' + dauerauftragLoeschen.id)).subscribe(
      data => {
        this.notification.handleServerResult(data, 'Löschen des gemeinsamen Dauerauftrags');
        this.refresh();
      },
      error => {
        this.notification.handleError(error, ERROR_RESULT, 'Löschen des gemeinsamen Dauerauftrags');
        this.refresh();
      }
  );
  }
}
