import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AllebuchungenComponent } from './allebuchungen.component';
import { MatChipsModule, MatButtonModule, MatCardModule, MatIconModule, MatSnackBarModule, MatFormFieldModule, MatTableModule } from '@angular/material';
import { LoginComponent } from '../auth/login/login.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MobileComponent } from '../sidebar/mobile/mobile.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('AllebuchungenComponent', () => {
  let component: AllebuchungenComponent;
  let fixture: ComponentFixture<AllebuchungenComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        LoginComponent,
        SidebarComponent,
        AllebuchungenComponent,
        MobileComponent,
      ],
      imports: [
        HttpClientTestingModule,
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
    fixture = TestBed.createComponent(AllebuchungenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
