import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {MatSelectModule,
  MatCheckboxModule,
  MatButtonModule,
  MatCardModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatSlideToggleModule,
  MatDatepickerModule,
  MatNativeDateModule,
  DateAdapter,
  MAT_DATE_LOCALE,
  ShowOnDirtyErrorStateMatcher,
  ErrorStateMatcher,
  MatTableModule,
  MatSortModule,
  MatChipsModule,
  MatSnackBarModule} from '@angular/material';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import { AppComponent } from './app.component';;

import { AppRoutingModule } from './app-routing.module';
import { LoginComponent } from './auth/login/login.component';
import { HttpClientModule } from '@angular/common/http';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { ChartsModule } from 'ng2-charts';
import { AddausgabeComponent } from './addausgabe/addausgabe.component';
import { AllebuchungenComponent } from './allebuchungen/allebuchungen.component';
import { MobileComponent } from './sidebar/mobile/mobile.component';
import { SettingsComponent } from './settings/settings.component';
import { AdduserComponent } from './settings/adduser/adduser.component';
import { AddeinnahmeComponent } from './addeinnahme/addeinnahme.component';
import { PartnernameComponent } from './settings/partnername/partnername.component';
import { AddgemeinsameausgabeComponent } from './addgemeinsameausgabe/addgemeinsameausgabe.component';
import { AllegemeinsamebuchungenComponent } from './allegemeinsamebuchungen/allegemeinsamebuchungen.component';

export const ALL_IMPORTS = [
  BrowserModule,
  FormsModule,
  ChartsModule,
  MatSlideToggleModule,
  MatSelectModule,
  MatButtonModule,
  MatDatepickerModule,
  MatNativeDateModule,
  MatCheckboxModule,
  MatButtonModule,
  MatChipsModule,
  MatCardModule,
  MatSnackBarModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatTableModule,
  MatSortModule,
  ReactiveFormsModule,
  BrowserAnimationsModule,
  AppRoutingModule,
  HttpClientModule
]


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    SidebarComponent,
    AddausgabeComponent,
    AllebuchungenComponent,
    MobileComponent,
    SettingsComponent,
    AdduserComponent,
    AddeinnahmeComponent,
    PartnernameComponent,
    AddgemeinsameausgabeComponent,
    AllegemeinsamebuchungenComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ChartsModule,
    MatSlideToggleModule,
    MatSelectModule,
    MatButtonModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatCheckboxModule,
    MatButtonModule,
    MatChipsModule,
    MatCardModule,
    MatSnackBarModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatTableModule,
    MatSortModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule
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
