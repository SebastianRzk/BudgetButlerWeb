import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MyErrorStateMatcher } from 'src/app/matcher';
import { AdminService } from '../../auth/admin.service';
import { PASSWOERTER_NICHT_GLEICH, PASSWORT_ZU_KURZ } from '../../errormessages';

@Component({
  selector: 'app-adduser',
  templateUrl: './adduser.component.html',
  styleUrls: ['./adduser.component.css']
})
export class AdduserComponent implements OnInit {

  public errorMatcher = new MyErrorStateMatcher();

  public username = new FormControl('', Validators.required);
  public email = new FormControl('', Validators.required);
  public passwort = new FormControl('', Validators.required);
  public passwortWiederholung = new FormControl('', Validators.required);

  public errorMessage = '';

  public isAdmin: Promise<boolean>;

  constructor(private adminService: AdminService) { }

  ngOnInit() {
    this.isAdmin = this.adminService.isAdmin();
  }

  computeErrorMesage = () => {
    if (this.passwort.value.length < 8) {
      this.errorMessage = PASSWORT_ZU_KURZ;
      return;
    }

    if (this.passwort.value !== this.passwortWiederholung.value) {
      this.errorMessage = PASSWOERTER_NICHT_GLEICH;
      return;
    }

    this.errorMessage = '';
  }

  addUser() {
    this.computeErrorMesage();

    if (this.errorMessage === '' && this.email.value !== '' &&  this.username.value !== '') {
      this.adminService.addUser(this.username.value, this.email.value, this.passwort.value);
    }

    this.email.setValue('');
    this.username.setValue('');
    this.passwort.setValue('');
    this.passwortWiederholung.setValue('');
  }

}
