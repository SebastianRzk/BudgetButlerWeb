import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PartnernameComponent } from './partnername.component';
import { MatCardModule, MatFormFieldModule, MatButtonModule, MatInputModule, MatCheckboxModule, MatSnackBarModule } from '@angular/material';
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
