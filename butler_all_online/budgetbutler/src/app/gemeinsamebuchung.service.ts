import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ApiproviderService } from './apiprovider.service';
import { toGemeinsameBuchungAnlegenTO } from './converter';
import { Einzelbuchung, ERROR_RESULT, GemeinsameBuchungLoeschen, Result, GemeinsameBuchungAnlegen } from './model';
import { NotificationService } from './notification.service';

@Injectable({
  providedIn: 'root'
})
export class GemeinsamebuchungService {

  constructor(private httpClient: HttpClient, private api: ApiproviderService, private notification: NotificationService) { }

  public save(buchung: GemeinsameBuchungAnlegen) {
    this.httpClient.put<Result>(this.api.getUrl('gemeinsamebuchung.php'), toGemeinsameBuchungAnlegenTO(buchung)).toPromise().then(
      data => this.notification.handleServerResult(data, 'Speichern der Ausgabe'),
      error => this.notification.handleServerResult(ERROR_RESULT, 'Speichern der Ausgabe')
    );
  }

  public getAll() {
    return this.httpClient.get<Einzelbuchung[]>(this.api.getUrl('gemeinsamebuchung.php'));
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
