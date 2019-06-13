import { Injectable } from '@angular/core';
import { Result } from './model';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  constructor(private snackBar: MatSnackBar) { }

  public handleServerResult(result: Result, actionDescription: string) {
    this.log(result, actionDescription);
    return result;
  }

  public log(result: Result, actionDescription: string) {
    this.snackBar.open(result.message, '', {duration: 3000});

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
