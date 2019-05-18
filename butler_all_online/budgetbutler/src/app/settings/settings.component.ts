import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { NotEmptyErrorStateMatcher } from '../matcher';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {

  public altesPasswort = new FormControl('', Validators.required);
  public neuesPasswort = new FormControl('', Validators.required);
  public neuesPasswortWiederholung = new FormControl('', Validators.required);

  public passwortMatcher = new NotEmptyErrorStateMatcher();

  public errorMessage = '';

  constructor() { }

  ngOnInit() {
  }

}
