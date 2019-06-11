import { HttpClientTestingModule } from '@angular/common/http/testing';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule, MatCardModule, MatDatepickerModule, MatFormFieldModule, MatIconModule, MatInputModule, MatNativeDateModule, MatSelectModule, MatSnackBarModule } from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MobileComponent } from '../sidebar/mobile/mobile.component';
import { AddgemeinsameausgabeComponent } from './addgemeinsameausgabe.component';


describe('AddgemeinsameausgabeComponent', () => {
  let component: AddgemeinsameausgabeComponent;
  let fixture: ComponentFixture<AddgemeinsameausgabeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AddgemeinsameausgabeComponent,
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
    fixture = TestBed.createComponent(AddgemeinsameausgabeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
