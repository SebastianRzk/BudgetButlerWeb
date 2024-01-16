import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {ApiproviderService} from './apiprovider.service';
import {KategorieTo} from "./modelTo";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class KategorieService {

  constructor(private httpClient: HttpClient, private api: ApiproviderService) {
  }

  public getAll() {
    return this.httpClient.get<KategorieTo[]>(this.api.getUrl('kategorien'))
      .pipe(map(kategorien => kategorien.map(kategorie => kategorie.name)));
  }


}
