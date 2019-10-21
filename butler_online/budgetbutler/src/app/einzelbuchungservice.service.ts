import { Injectable } from '@angular/core';
import { Einzelbuchung, Result, ERROR_RESULT, EinzelbuchungLoeschen, EinzelbuchungAnlegen } from './model';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ApiproviderService } from './apiprovider.service';
import { NotificationService } from './notification.service';
import { toEinzelbuchungAnlegenTO } from './converter';

@Injectable({
  providedIn: 'root'
})
export class EinzelbuchungserviceService {

  constructor(private httpClient: HttpClient, private api: ApiproviderService, private notification: NotificationService) { }

  public save(einzelBuchung: EinzelbuchungAnlegen) {
    this.httpClient.put<Result>(this.api.getUrl('einzelbuchung.php'), toEinzelbuchungAnlegenTO(einzelBuchung)).toPromise().then(
      data => this.notification.handleServerResult(data, 'Speichern der Ausgabe'),
      error => this.notification.handleServerResult(ERROR_RESULT, 'Speichern der Ausgabe')
    );
  }

  public getAll() {
    return this.httpClient.get<Einzelbuchung[]>(this.api.getUrl('einzelbuchung.php'));
  }

  public delete(einzelbuchungLoeschen: EinzelbuchungLoeschen){
    const httpOptions = {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }), body: einzelbuchungLoeschen
     };
    this.httpClient.delete<Result>(this.api.getUrl('einzelbuchung.php'), httpOptions).toPromise().then(
      data => this.notification.handleServerResult(data, 'Löschen der Ausgabe'),
      error => this.notification.handleServerResult(ERROR_RESULT, 'Löschen der Ausgabe')
    );
  }

}
