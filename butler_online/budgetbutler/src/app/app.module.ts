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
import {PartnernameComponent} from './pages/settings/partnername/partnername.component';
import {AllegemeinsamebuchungenComponent} from './pages/allegemeinsamebuchungen/allegemeinsamebuchungen.component';
import {AddBuchungComponent} from './pages/addbuchung/add-buchung.component';
import {SidebarToggleComponent} from './pages/sidebar/sidebar-toggle/sidebar-toggle.component';
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import { LogoutComponent } from './pages/auth/logout/logout.component';
import { OfflineLoginComponent } from './pages/offline-login/offline-login.component';
import { AddDauerauftragComponent } from './pages/adddauerauftrag/add-dauerauftrag.component';
import {DauerauftraegeComponent} from "./pages/dauerauftraege/dauerauftraege.component";
import {GemeinsameDauerauftraegeComponent} from "./pages/gemeinsame-dauerauftraege/gemeinsame-dauerauftraege.component";
import { KategorienComponent } from './pages/kategorien/kategorien.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SidebarComponent,
    AllebuchungenComponent,
    SettingsComponent,
    PartnernameComponent,
    AllegemeinsamebuchungenComponent,
    AddBuchungComponent,
    SidebarToggleComponent,
    LogoutComponent,
    OfflineLoginComponent,
    AddDauerauftragComponent,
    DauerauftraegeComponent,
    GemeinsameDauerauftraegeComponent,
    KategorienComponent
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
        MatChipsModule,
        MatProgressSpinnerModule
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
