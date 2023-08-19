import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpClient } from '@angular/common/http';
import { ApiproviderService } from '../../domain/apiprovider.service';
import { Result } from '../../domain/model';
import { NotificationService } from '../../domain/notification.service';
import { AddUserDataTo } from '../../domain/modelTo';

@Injectable({
  providedIn: 'root'
})
export class AdminService {

  constructor(
    private authService: AuthService,
    private httpClient: HttpClient,
    private apiprovider: ApiproviderService,
    private notificationService: NotificationService) {
  }


  public async isAdmin() {
    const x = await this.authService.getLogin().toPromise();
    return x.role === 'admin';
  }


  public addUser: (username: string, email: string, password: string) => void = (username: string, email: string, password: string) => {
    const data: AddUserDataTo = {
      username,
      email,
      password
    };

    this.httpClient
      .post<Result>(this.apiprovider.getUrl('adduser.php'), data).toPromise()
      .then(result => this.notificationService.handleServerResult(result, 'Erstelle Benutzer'));

  }
}



