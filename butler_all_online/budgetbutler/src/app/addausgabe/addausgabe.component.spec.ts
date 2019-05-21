import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LoginComponent } from '../auth/login/login.component';
import { MobileComponent } from '../sidebar/mobile/mobile.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { AddausgabeComponent } from './addausgabe.component';
import { MatSelectModule, MatButtonModule, MatDatepickerModule, MatNativeDateModule, MatCardModule, MatFormFieldModule, MatIconModule, MatInputModule, MatSnackBarModule } from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {HttpClientTestingModule} from '@angular/common/http/testing';


describe('AddausgabeComponent', () => {
  let component: AddausgabeComponent;
  let fixture: ComponentFixture<AddausgabeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        LoginComponent,
        SidebarComponent,
        AddausgabeComponent,
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
        MatInputModule,
        MatSnackBarModule,
        ReactiveFormsModule,
        BrowserAnimationsModule,
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddausgabeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
