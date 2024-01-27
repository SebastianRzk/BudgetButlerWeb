import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LocalStorageService {


  private readonly LOCAL_LOGIN_KEY = 'butler.local.login';

  private readonly VALUE_POSITIVE = 'true';

  setOfflineLogin(){
      localStorage.setItem(this.LOCAL_LOGIN_KEY, this.VALUE_POSITIVE);
  }

  isOfflineLogin() : boolean{
    return localStorage.getItem(this.LOCAL_LOGIN_KEY) === this.VALUE_POSITIVE;
  }

  removeLocalLogin(){
    localStorage.removeItem(this.LOCAL_LOGIN_KEY);
  }





}
