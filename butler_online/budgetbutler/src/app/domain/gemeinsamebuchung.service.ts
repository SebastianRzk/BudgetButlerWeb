import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ApiproviderService } from './apiprovider.service';
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

  private gemeinsamebuchungen = new BehaviorSubject<GemeinsameBuchung[]>([]);

  public readonly gemeinsameBuchungen$ = this.gemeinsamebuchungen.asObservable();

  constructor(private httpClient: HttpClient, private api: ApiproviderService, private notification: NotificationService) {
  }

  public save(buchung: GemeinsameBuchungAnlegen) {
    this.httpClient.put<Result>(this.api.getUrl('gemeinsamebuchung.php'), toGemeinsameBuchungAnlegenTO(buchung)).toPromise().then(
      data => this.notification.handleServerResult(data, 'Speichern der Ausgabe'),
      error => this.notification.handleServerResult(ERROR_RESULT, 'Speichern der Ausgabe')
    );
  }

  public refresh(): void {
    this.httpClient.get<GemeinsameBuchungTO[]>(this.api.getUrl('gemeinsamebuchung.php'))
      .pipe(map((dtos: GemeinsameBuchungTO[]) => dtos.map(toGemeinsameBuchung)))
      .subscribe(
        x => this.gemeinsamebuchungen.next(x),
        error => this.notification.log(ERROR_LOADING_GEMEINSAME_BUCHUNGEN, ERROR_LOADING_GEMEINSAME_BUCHUNGEN.message));
  }

  public delete(buchung: GemeinsameBuchungLoeschen) {
    const httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'}), body: buchung
    };
    this.httpClient.delete<Result>(this.api.getUrl('gemeinsamebuchung.php'), httpOptions).toPromise().then(
      data => {
        this.notification.handleServerResult(data, 'Löschen der Ausgabe');
        this.refresh();
      },
      error => {
        this.notification.handleServerResult(ERROR_RESULT, 'Löschen der Ausgabe');
        this.refresh();
      }
    );
  }

}
