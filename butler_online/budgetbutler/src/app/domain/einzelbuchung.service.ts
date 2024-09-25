import { inject, Injectable } from '@angular/core';
import {
  Einzelbuchung,
  EinzelbuchungAnlegen,
  EinzelbuchungLoeschen,
  ERROR_LOADING_EINZELBUCHUNGEN,
  ERROR_RESULT,
  Result
} from './model';
import { HttpClient } from '@angular/common/http';
import { ApiProviderService } from './api-provider.service';
import { NotificationService } from './notification.service';
import { toEinzelbuchung, toEinzelbuchungAnlegenTO } from './mapper';
import { BehaviorSubject } from 'rxjs';
import { EinzelbuchungTO } from './modelTo';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class EinzelbuchungService {

  private httpClient: HttpClient = inject(HttpClient);
  private api: ApiProviderService = inject(ApiProviderService);
  private notification: NotificationService = inject(NotificationService);
  private einzelbuchungen = new BehaviorSubject<Einzelbuchung[]>([]);
  public readonly einzelbuchungen$ = this.einzelbuchungen.asObservable();


  public save(einzelBuchung: EinzelbuchungAnlegen) {
    this.httpClient.post<Result>(this.api.getUrl('einzelbuchung'), toEinzelbuchungAnlegenTO(einzelBuchung)).subscribe(
      data => this.notification.handleServerResult(data, 'Speichern der Ausgabe'),
      error => this.notification.handleError(error, ERROR_RESULT, 'Speichern der Ausgabe')
    );
  }


  public refresh(): void {
    this.httpClient.get<EinzelbuchungTO[]>(this.api.getUrl('einzelbuchungen')).pipe(map(x => x.map(toEinzelbuchung))).subscribe(
      x => this.einzelbuchungen.next(x),
      error => this.notification.handleError(error, ERROR_LOADING_EINZELBUCHUNGEN, ERROR_LOADING_EINZELBUCHUNGEN.message));
  }

  public delete(einzelbuchungLoeschen: EinzelbuchungLoeschen) {
    this.httpClient.delete<Result>(this.api.getUrl('einzelbuchung/' + einzelbuchungLoeschen.id)).subscribe(
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
