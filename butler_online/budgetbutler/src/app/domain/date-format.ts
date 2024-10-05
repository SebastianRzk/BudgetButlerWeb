import {NativeDateAdapter} from "@angular/material/core";

export class EuropeanNativeDateAdapter extends NativeDateAdapter {
  override getFirstDayOfWeek(): number {
    return 1;//Monday
  }
}
