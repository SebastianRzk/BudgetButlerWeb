import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LocalStorageService {


  private readonly LOCAL_LOGIN_KEY = 'butler.local.login';

  private readonly LOCAL_LOGIN_URL_KEY = 'butler.local.login.url';

  private readonly VALUE_POSITIVE = 'true';

  setOfflineLogin(url: string) {
    console.log('setOfflineLogin true with login url', url);
    localStorage.setItem(this.LOCAL_LOGIN_KEY, this.VALUE_POSITIVE);
    localStorage.setItem(this.LOCAL_LOGIN_URL_KEY, url);
  }

  isOfflineLogin(): boolean {
    console.log('isOfflineLogin', localStorage.getItem(this.LOCAL_LOGIN_KEY));
    return localStorage.getItem(this.LOCAL_LOGIN_KEY) === this.VALUE_POSITIVE;
  }

  getLocalLoginUrl() {
    console.log('getLocalLoginUrl', localStorage.getItem(this.LOCAL_LOGIN_URL_KEY));
    return localStorage.getItem(this.LOCAL_LOGIN_URL_KEY);
  }

  removeLocalLogin() {
    console.log('removeLocalLogin');
    localStorage.removeItem(this.LOCAL_LOGIN_KEY);
    localStorage.removeItem(this.LOCAL_LOGIN_URL_KEY);
  }


}
