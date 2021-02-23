import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpClient } from '@angular/common/http';
import { ApiproviderService } from '../apiprovider.service';
import { Result } from '../model';
import { NotificationService } from '../notification.service';

@Injectable({
  providedIn: 'root'
})
export class AdminService {

  constructor(
    private authService: AuthService,
    private httpClient: HttpClient,
    private apiprovider: ApiproviderService,
    private notificationService: NotificationService) { }


  public isAdmin: () => Promise<boolean> = () => {
    return this.authService.getLogin().toPromise().then(x => x.role === 'admin');
  }


  public addUser: (username: string, email: string, password: string) => void = (username: string, email: string, password: string) => {
    const data: AddUserData = {
      username,
      email,
      password
    }

    this.httpClient.
      post<Result>(this.apiprovider.getUrl('adduser.php'), data).
      toPromise().then(result => this.notificationService.handleServerResult(result, 'Erstelle Benutzer'));

  }
}


interface AddUserData {
  username: string;
  email: string;
  password: string;
};