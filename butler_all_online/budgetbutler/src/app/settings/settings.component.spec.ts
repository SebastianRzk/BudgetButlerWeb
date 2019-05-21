import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SettingsComponent } from './settings.component';
import { LoginComponent } from '../auth/login/login.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MobileComponent } from '../sidebar/mobile/mobile.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule, MatButtonModule, MatDatepickerModule, MatNativeDateModule, MatCardModule, MatFormFieldModule, MatIconModule, MatInputModule, MatSnackBarModule, MatChipsModule } from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('SettingsComponent', () => {
  let component: SettingsComponent;
  let fixture: ComponentFixture<SettingsComponent>;

  const onePassword = '123456789';
  const tooShortPassword = '123';
  const anotherPassword = '123456789abc';

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        LoginComponent,
        SidebarComponent,
        SettingsComponent,
        MobileComponent,
      ],
      imports: [
        HttpClientTestingModule,
        FormsModule,
        MatSelectModule,
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
    expect(component.errorMessage).toEqual('Bitte altes Passwort eingeben.');
  });

  it('should show error message when no new pw given', () => {
    component.altesPasswort.setValue(onePassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual('Das neue Passwort muss mehr als 8 Zeichen lang sein.');
  });

  it('should show error message when all pw are equal', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(onePassword);
    component.neuesPasswortWiederholung.setValue(onePassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual('Das alte und das neue Passwort dürfen nicht identisch sein.');
  });

  it('should show error message when new pw to short', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(tooShortPassword);
    component.neuesPasswortWiederholung.setValue(tooShortPassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual('Das neue Passwort muss mehr als 8 Zeichen lang sein.');
  });

  it('should show error message when new pws are not equal', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(anotherPassword);
    component.neuesPasswortWiederholung.setValue(anotherPassword + 'wrong');
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual('Passwörter sind nicht identisch.');
  });

  it('should show no error message when everything is ok', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(anotherPassword);
    component.neuesPasswortWiederholung.setValue(anotherPassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual('');
  });

});
