import { HttpClientTestingModule } from '@angular/common/http/testing';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from '@angular/material/chips';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterTestingModule } from '@angular/router/testing';
import { ALTES_PASSWORT_FEHLT, PASSWOERTER_NICHT_GLEICH, PASSWORT_IDENTISCH, PASSWORT_ZU_KURZ } from '../errormessages';
import { AdduserComponent } from './adduser/adduser.component';
import { PartnernameComponent } from './partnername/partnername.component';
import { SettingsComponent } from './settings.component';


describe('SettingsComponent', () => {
  let component: SettingsComponent;
  let fixture: ComponentFixture<SettingsComponent>;

  const onePassword = '123456789';
  const tooShortPassword = '123';
  const anotherPassword = '123456789abc';

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        SettingsComponent,
        AdduserComponent,
        PartnernameComponent,
      ],
      imports: [
        HttpClientTestingModule,
        FormsModule,
        MatSelectModule,
        MatCheckboxModule,
        MatButtonModule,
        MatDatepickerModule,
        MatNativeDateModule,
        MatButtonModule,
        MatCardModule,
        MatFormFieldModule,
        MatIconModule,
        MatChipsModule,
        MatInputModule,
        MatSnackBarModule,
        ReactiveFormsModule,
        RouterTestingModule,
        BrowserAnimationsModule,
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should show error message when nothing given', () => {
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(ALTES_PASSWORT_FEHLT);
  });

  it('should show error message when no new pw given', () => {
    component.altesPasswort.setValue(onePassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(PASSWORT_ZU_KURZ);
  });

  it('should show error message when all pw are equal', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(onePassword);
    component.neuesPasswortWiederholung.setValue(onePassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(PASSWORT_IDENTISCH);
  });

  it('should show error message when new pw to short', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(tooShortPassword);
    component.neuesPasswortWiederholung.setValue(tooShortPassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(PASSWORT_ZU_KURZ);
  });

  it('should show error message when new pws are not equal', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(anotherPassword);
    component.neuesPasswortWiederholung.setValue(anotherPassword + 'wrong');
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(PASSWOERTER_NICHT_GLEICH);
  });

  it('should show no error message when everything is ok', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(anotherPassword);
    component.neuesPasswortWiederholung.setValue(anotherPassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual('');
  });

});
