import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AllegemeinsamebuchungenComponent } from './allegemeinsamebuchungen.component';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { LoginComponent } from '../auth/login/login.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MobileComponent } from '../sidebar/mobile/mobile.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterTestingModule } from '@angular/router/testing';
import { MoreComponent } from '../sidebar/mobile/more/more.component';

describe('AllebuchungenComponent', () => {
  let component: AllegemeinsamebuchungenComponent;
  let fixture: ComponentFixture<AllegemeinsamebuchungenComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        LoginComponent,
        SidebarComponent,
        AllegemeinsamebuchungenComponent,
        MobileComponent,
        MoreComponent,
      ],
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
        FormsModule,
        MatChipsModule,
        MatButtonModule,
        MatCardModule,
        MatIconModule,
        MatFormFieldModule,
        MatTableModule,
        MatSnackBarModule,
        ReactiveFormsModule,
        BrowserAnimationsModule,
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllegemeinsamebuchungenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
