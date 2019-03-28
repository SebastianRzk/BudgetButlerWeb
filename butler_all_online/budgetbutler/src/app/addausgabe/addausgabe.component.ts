import { Component, OnInit } from '@angular/core';
import { Einzelbuchung } from '../model';
import { EinzelbuchungserviceService } from '../einzelbuchungservice.service';
import { NotificationService } from '../notification.service';
import { FormControl, FormGroupDirective, NgForm, Validators } from '@angular/forms';
import { toEinzelbuchungTO } from '../converter';
import { ErrorStateMatcher } from '@angular/material';

export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}


@Component({
  selector: 'app-addausgabe',
  templateUrl: './addausgabe.component.html',
  styleUrls: ['./addausgabe.component.css']
})
export class AddausgabeComponent implements OnInit {

  datum = new FormControl(new Date(), Validators.required);
  name = new FormControl('', Validators.required);
  kategorie = new FormControl('saab', Validators.required);
  wert = new FormControl('', Validators.required);
  matcher = new MyErrorStateMatcher();

  constructor(private einzelbuchungsService: EinzelbuchungserviceService, private notification: NotificationService) { }

  ngOnInit() {
  }

  hinzufuegen() {
    if (this.matcher.isErrorState) {
      return;
    }

    const neueBuchung: Einzelbuchung = {
      id: 0,
      name: this.name.value,
      datum: this.datum.value,
      kategorie: this.kategorie.value,
      wert: this.wert.value
    };

    this.einzelbuchungsService.save(neueBuchung);
}

}
