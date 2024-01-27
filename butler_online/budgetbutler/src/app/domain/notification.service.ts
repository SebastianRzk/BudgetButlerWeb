import { inject, Injectable } from '@angular/core';
import {Result} from './model';
import {MatSnackBar} from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  private snackBar: MatSnackBar = inject(MatSnackBar);

  public handleServerResult(result: Result, actionDescription: string) {
    this.log(result, actionDescription);
    return result;
  }
  public handleError(error: unknown, result: Result, actionDescription: string) {
    console.log(error);
    return this.handleServerResult(result, actionDescription);
  }

  public log(result: Result, actionDescription: string) {
    this.snackBar.open(result.message, '', {duration: 3000});

    console.log('----------');
    console.log(result);
    console.log(actionDescription);
    console.log('----------');
  }
}
