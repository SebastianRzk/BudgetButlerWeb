import { Injectable } from '@angular/core';
import { Result } from './model';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  constructor() { }

  public handleServerResult(result: Result, actionDescription: string) {
    this.log(result, actionDescription);
  }

  public log(result: Result, actionDescription: string) {
    console.log('----------');
    console.log(result);
    console.log(actionDescription);
    console.log('----------');
  }

  public logSomething(obj: any) {
    console.log('----------');
    console.log(obj);
    console.log('----------');
  }
}
