import { inject, Injectable } from '@angular/core';
import { BuchungsUebersicht, ERROR_LOADING_UEBERSICHT } from './model';
import { HttpClient } from '@angular/common/http';
import { ApiProviderService } from './api-provider.service';
import { NotificationService } from './notification.service';
import { toBuchungsUebersicht } from './mapper';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { BuchungsUebersichtTO } from './modelTo';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class GemeinsameBuchungenUebersichtService {

  private httpClient: HttpClient = inject(HttpClient);
  private api: ApiProviderService = inject(ApiProviderService);
  private notification: NotificationService = inject(NotificationService);
  private einzelbuchungenUebersicht = new BehaviorSubject<BuchungsUebersicht>({
    monate: []
  });
  public readonly gemeinsameBuchungenUebersicht$ = this.einzelbuchungenUebersicht.asObservable();


  public refresh(): void {
    firstValueFrom(this.httpClient.get<BuchungsUebersichtTO>(this.api.getUrl('gemeinsame_buchungen_uebersicht')).pipe(map(x => toBuchungsUebersicht(x)))).then(
      x => this.einzelbuchungenUebersicht.next(x),
      error => this.notification.handleError(error, ERROR_LOADING_UEBERSICHT, ERROR_LOADING_UEBERSICHT.message));
  }


}
