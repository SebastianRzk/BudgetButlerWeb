import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatChipsModule} from '@angular/material/chips';
import {DateAdapter, ErrorStateMatcher, MatNativeDateModule, ShowOnDirtyErrorStateMatcher} from '@angular/material/core';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatSortModule} from '@angular/material/sort';
import {MatTableModule} from '@angular/material/table';
import {MatSidenavModule} from '@angular/material/sidenav';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import {AppComponent} from './app.component';
import {AppRoutingModule} from './app-routing.module';
import {LoginComponent} from './pages/auth/login/login.component';
import {HttpClientModule} from '@angular/common/http';
import {SidebarComponent} from './pages/sidebar/sidebar/sidebar.component';
import {AllebuchungenComponent} from './pages/allebuchungen/allebuchungen.component';
import {SettingsComponent} from './pages/settings/settings.component';
import {AdduserComponent} from './pages/settings/adduser/adduser.component';
import {PartnernameComponent} from './pages/settings/partnername/partnername.component';
import {AllegemeinsamebuchungenComponent} from './pages/allegemeinsamebuchungen/allegemeinsamebuchungen.component';
import {AddschnelleinstiegComponent} from './pages/addschnelleinstieg/addschnelleinstieg.component';
import {SidebarToggleComponent} from './pages/sidebar/sidebar-toggle/sidebar-toggle.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SidebarComponent,
    AllebuchungenComponent,
    SettingsComponent,
    AdduserComponent,
    PartnernameComponent,
    AllegemeinsamebuchungenComponent,
    AddschnelleinstiegComponent,
    SidebarToggleComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    MatSlideToggleModule,
    MatSelectModule,
    MatButtonModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatCheckboxModule,
    MatChipsModule,
    MatCardModule,
    MatSidenavModule,
    MatSnackBarModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatTableModule,
    MatSortModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    MatChipsModule
  ],
  providers: [
    {provide: ErrorStateMatcher, useClass: ShowOnDirtyErrorStateMatcher}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(private dateAdapter: DateAdapter<Date>) {
    this.dateAdapter.setLocale('de');
    this.dateAdapter.getFirstDayOfWeek = () => 1;
  }

}
