import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ApiProviderService } from './api-provider.service';
import { toGemeinsameBuchung, toGemeinsameBuchungAnlegenTO } from './mapper';
import {
  ERROR_LOADING_GEMEINSAME_BUCHUNGEN,
  ERROR_RESULT,
  GemeinsameBuchung,
  GemeinsameBuchungAnlegen,
  GemeinsameBuchungLoeschen,
  Result
} from './model';
import { NotificationService } from './notification.service';
import { GemeinsameBuchungTO } from './modelTo';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class GemeinsamebuchungService {

  private httpClient: HttpClient = inject(HttpClient);
  private api: ApiProviderService = inject(ApiProviderService);
  private notification: NotificationService = inject(NotificationService);

  private gemeinsamebuchungen = new BehaviorSubject<GemeinsameBuchung[]>([]);

  public readonly gemeinsameBuchungen$ = this.gemeinsamebuchungen.asObservable();

  public save(buchung: GemeinsameBuchungAnlegen) {
    this.httpClient.post<Result>(this.api.getUrl('gemeinsame_buchung'), toGemeinsameBuchungAnlegenTO(buchung)).subscribe(
      data => this.notification.handleServerResult(data, 'Speichern der Ausgabe'),
      error => this.notification.handleError(error, ERROR_RESULT, 'Speichern der Ausgabe')
    );
  }

  public refresh(): void {
    this.httpClient.get<GemeinsameBuchungTO[]>(this.api.getUrl('gemeinsame_buchungen'))
      .pipe(map((dtos: GemeinsameBuchungTO[]) => dtos.map(toGemeinsameBuchung)))
      .subscribe(
        x => this.gemeinsamebuchungen.next(x),
        error => this.notification.handleError(error, ERROR_LOADING_GEMEINSAME_BUCHUNGEN, ERROR_LOADING_GEMEINSAME_BUCHUNGEN.message));
  }

  public delete(buchung: GemeinsameBuchungLoeschen) {
    this.httpClient.delete<Result>(this.api.getUrl('gemeinsame_buchung/' + buchung.id)).subscribe(
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
