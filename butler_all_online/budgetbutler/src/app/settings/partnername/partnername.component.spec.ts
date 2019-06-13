import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PartnernameComponent } from './partnername.component';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('PartnernameComponent', () => {
  let component: PartnernameComponent;
  let fixture: ComponentFixture<PartnernameComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [PartnernameComponent],
      imports: [MatCardModule, MatFormFieldModule, MatButtonModule, MatInputModule, MatCheckboxModule, MatSnackBarModule,
        ReactiveFormsModule, FormsModule, BrowserAnimationsModule,
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
