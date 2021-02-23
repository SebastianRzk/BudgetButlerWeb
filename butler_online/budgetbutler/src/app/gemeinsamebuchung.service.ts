import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { ApiproviderService } from './apiprovider.service';
import { toGemeinsameBuchungAnlegenTO } from './converter';
import { ERROR_RESULT, ERROR_LOADING_GEMEINSAME_BUCHUNGEN, GemeinsameBuchungLoeschen, Result, GemeinsameBuchungAnlegen, GemeinsameBuchung } from './model';
import { NotificationService } from './notification.service';

@Injectable({
  providedIn: 'root'
})
export class GemeinsamebuchungService {

  private gemeinsamebuchungen = new BehaviorSubject<GemeinsameBuchung[]>([]);

  constructor(private httpClient: HttpClient, private api: ApiproviderService, private notification: NotificationService) { }

  public save(buchung: GemeinsameBuchungAnlegen) {
    this.httpClient.put<Result>(this.api.getUrl('gemeinsamebuchung.php'), toGemeinsameBuchungAnlegenTO(buchung)).toPromise().then(
      data => this.notification.handleServerResult(data, 'Speichern der Ausgabe'),
      error => this.notification.handleServerResult(ERROR_RESULT, 'Speichern der Ausgabe')
    );
  }

  public getAll(): Subject<GemeinsameBuchung[]> {
    return this.gemeinsamebuchungen;
  }

  public refresh(): void {
    this.httpClient.get<GemeinsameBuchung[]>(this.api.getUrl('gemeinsamebuchung.php')).subscribe(
      x => this.gemeinsamebuchungen.next(x),
      error => this.notification.log(ERROR_LOADING_GEMEINSAME_BUCHUNGEN, ERROR_LOADING_GEMEINSAME_BUCHUNGEN.message));
  }

  public delete(buchung: GemeinsameBuchungLoeschen){
    const httpOptions = {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }), body: buchung
     };
    this.httpClient.delete<Result>(this.api.getUrl('gemeinsamebuchung.php'), httpOptions).toPromise().then(
      data => this.notification.handleServerResult(data, 'Löschen der Ausgabe'),
      error => this.notification.handleServerResult(ERROR_RESULT, 'Löschen der Ausgabe')
    );
  }

}
