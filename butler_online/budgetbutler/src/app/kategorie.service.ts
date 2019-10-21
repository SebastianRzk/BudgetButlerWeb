import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ApiproviderService } from './apiprovider.service';

@Injectable({
  providedIn: 'root'
})
export class KategorieService {

  constructor(private httpClient: HttpClient, private api: ApiproviderService) { }

  public getAll() {
    return this.httpClient.get<string[]>(this.api.getUrl('kategorie.php'));
  }


}
