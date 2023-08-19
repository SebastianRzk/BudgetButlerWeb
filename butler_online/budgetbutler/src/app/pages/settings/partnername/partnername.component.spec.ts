import {ComponentFixture, TestBed, waitForAsync} from '@angular/core/testing';

import {PartnernameComponent} from './partnername.component';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientTestingModule} from '@angular/common/http/testing';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {RouterTestingModule} from '@angular/router/testing';

describe('PartnernameComponent', () => {
  let component: PartnernameComponent;
  let fixture: ComponentFixture<PartnernameComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [PartnernameComponent],
      imports: [MatCardModule, MatFormFieldModule, MatButtonModule, MatInputModule, MatCheckboxModule, MatSnackBarModule,
        ReactiveFormsModule, FormsModule, BrowserAnimationsModule, RouterTestingModule,
        HttpClientTestingModule,
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PartnernameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
