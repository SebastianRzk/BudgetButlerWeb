import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { AdminService } from '../../auth/admin.service';
import { PASSWOERTER_NICHT_GLEICH, PASSWORT_ZU_KURZ } from '../errormessages';

@Component({
  selector: 'app-adduser',
  templateUrl: './adduser.component.html',
  styleUrls: ['./adduser.component.css']
})
export class AdduserComponent implements OnInit {

  newUserForm = new FormGroup({
    username: new FormControl('', Validators.required),
    email: new FormControl('', Validators.required),
    passwort: new FormControl('', Validators.required),
    passwortWiederholung: new FormControl('', Validators.required)
  });

  public errorMessage = '';

  public isAdmin: Promise<boolean>;

  constructor(private adminService: AdminService) { }

  ngOnInit() {
    this.isAdmin = this.adminService.isAdmin();
  }

  computeErrorMesage = () => {
    if (this.newUserForm.get('passwort').value.length < 8) {
      this.errorMessage = PASSWORT_ZU_KURZ;
      return;
    }

    if (this.newUserForm.get('passwort').value !== this.newUserForm.get('passwortWiederholung').value) {
      this.errorMessage = PASSWOERTER_NICHT_GLEICH;
      return;
    }

    this.errorMessage = '';
  }

  onNewUserSubmit() {
    this.computeErrorMesage();

    if (this.errorMessage !== '') {
      return;
    }

    if (!this.newUserForm.valid) {
      return;
    }

    this.adminService.addUser(this.newUserForm.get('username').value,
      this.newUserForm.get('email').value,
      this.newUserForm.get('passwort').value);

    this.newUserForm.reset();
  }

}
