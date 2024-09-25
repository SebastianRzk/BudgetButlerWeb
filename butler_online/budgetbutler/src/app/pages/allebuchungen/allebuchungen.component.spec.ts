import {ComponentFixture, TestBed, waitForAsync} from '@angular/core/testing';

import {AllebuchungenComponent} from './allebuchungen.component';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatChipsModule} from '@angular/material/chips';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatTableModule} from '@angular/material/table';
import {LoginComponent} from '../auth/login/login.component';
import {SidebarComponent} from '../sidebar/sidebar/sidebar.component';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

describe('AllebuchungenComponent', () => {
  let component: AllebuchungenComponent;
  let fixture: ComponentFixture<AllebuchungenComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
    imports: [FormsModule,
        MatChipsModule,
        MatButtonModule,
        MatCardModule,
        MatIconModule,
        MatFormFieldModule,
        MatTableModule,
        MatSnackBarModule,
        ReactiveFormsModule,
        BrowserAnimationsModule, LoginComponent,
        SidebarComponent,
        AllebuchungenComponent],
    providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()]
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
