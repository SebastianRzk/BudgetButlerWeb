import {Injectable} from '@angular/core';
import {Einzelbuchung, EinzelbuchungAnlegen, EinzelbuchungLoeschen, ERROR_LOADING_EINZELBUCHUNGEN, ERROR_RESULT, Result} from './model';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {ApiproviderService} from './apiprovider.service';
import {NotificationService} from './notification.service';
import {toEinzelbuchungAnlegenTO} from './mapper';
import {BehaviorSubject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EinzelbuchungService {

  private einzelbuchungen = new BehaviorSubject<Einzelbuchung[]>([]);
  public readonly einzelbuchungen$ = this.einzelbuchungen.asObservable();

  constructor(private httpClient: HttpClient, private api: ApiproviderService, private notification: NotificationService) {
  }

  public save(einzelBuchung: EinzelbuchungAnlegen) {
    this.httpClient.put<Result>(this.api.getUrl('einzelbuchung'), toEinzelbuchungAnlegenTO(einzelBuchung)).toPromise().then(
      data => this.notification.handleServerResult(data, 'Speichern der Ausgabe'),
      error => this.notification.handleServerResult(ERROR_RESULT, 'Speichern der Ausgabe')
    );
  }


  public refresh(): void {
    this.httpClient.get<Einzelbuchung[]>(this.api.getUrl('einzelbuchungen/')).subscribe(
      x => this.einzelbuchungen.next(x),
      error => this.notification.log(ERROR_LOADING_EINZELBUCHUNGEN, ERROR_LOADING_EINZELBUCHUNGEN.message));
  }

  public delete(einzelbuchungLoeschen: EinzelbuchungLoeschen) {
    this.httpClient.delete<Result>(this.api.getUrl('einzelbuchung/' + einzelbuchungLoeschen.id)).toPromise().then(
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
