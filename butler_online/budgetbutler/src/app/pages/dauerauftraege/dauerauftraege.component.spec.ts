import {ComponentFixture, TestBed, waitForAsync} from '@angular/core/testing';

import {DauerauftraegeComponent} from './dauerauftraege.component';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatChipsModule} from '@angular/material/chips';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatTableModule} from '@angular/material/table';
import {LoginComponent} from '../auth/login/login.component';
import {SidebarComponent} from '../sidebar/sidebar/sidebar.component';
import {HttpClientTestingModule} from '@angular/common/http/testing';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

describe('DauerauftraegeComponent', () => {
  let component: DauerauftraegeComponent;
  let fixture: ComponentFixture<DauerauftraegeComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [
        LoginComponent,
        SidebarComponent,
        DauerauftraegeComponent,
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
    fixture = TestBed.createComponent(DauerauftraegeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
