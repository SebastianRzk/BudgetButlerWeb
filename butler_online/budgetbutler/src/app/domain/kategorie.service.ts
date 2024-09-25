import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ApiProviderService } from './api-provider.service';
import { map } from 'rxjs/operators';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { ERROR_RESULT, Result } from './model';
import { NotificationService } from './notification.service';

@Injectable({
  providedIn: 'root'
})
export class KategorieService {

  private kategorien: Subject<Kategorie[]> = new BehaviorSubject<Kategorie[]>([]);
  private notification: NotificationService = inject(NotificationService);
  private httpClient: HttpClient = inject(HttpClient);
  private api: ApiProviderService = inject(ApiProviderService);
  kategorien$: Observable<Kategorie[]> = this.kategorien.asObservable();

  public refresh(): void {
    this.httpClient.get<KategorieTo[]>(this.api.getUrl('kategorien'))
      .pipe(map(x => x.map(this.mapFromTo)))
      .subscribe(x => this.kategorien.next(x));
  }

  public add(name: string): void {
    let headers = new HttpHeaders();
    headers = headers.set('Content-Type', 'application/json; charset=utf-8');
    this.httpClient.post<Result>(this.api.getUrl('kategorien'), `"${name}"`, {headers}).toPromise().then(
      data => {
        console.log(data);
        this.notification.handleServerResult({result: 'OK', message: 'Kategorie erfolgreich hinzugefügt'}, 'Speichern der Kategorie');
        this.refresh();
      },
      error => {
        this.notification.handleError(error, ERROR_RESULT, 'Speichern der Kategorie');
        this.refresh();
      }
    );
  }
  public delete(id: string): void {
    this.httpClient.delete<Result>(this.api.getUrl('kategorie/' + id)).toPromise().then(
      data => {
        console.log(data);
        this.notification.handleServerResult({result: 'OK', message: 'Kategorie erfolgreich gelöscht'}, 'Löschen der Kategorie');
        this.refresh();
      },
      error => {
        this.notification.handleError(error, ERROR_RESULT, 'Löschen der Kategorie');
        this.refresh();
      }
    );
  }

  private mapFromTo(to: KategorieTo): Kategorie {
    return {
      name: to.name,
      id: to.id
    };
  }
}


export interface Kategorie {
  name: string;
  id: string;
}

export interface KategorieTo {
  readonly id: string;
  readonly name: string;
  readonly user: string;
}
