import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthGuard } from './auth/auth.guard';
import { LoginComponent } from './auth/login/login.component';
import { AddausgabeComponent } from './addausgabe/addausgabe.component';
import { AllebuchungenComponent } from './allebuchungen/allebuchungen.component';
import { SettingsComponent } from './settings/settings.component';
import { AddeinnahmeComponent } from './addeinnahme/addeinnahme.component';
import { AddgemeinsameausgabeComponent } from './addgemeinsameausgabe/addgemeinsameausgabe.component';
import { AllegemeinsamebuchungenComponent } from './allegemeinsamebuchungen/allegemeinsamebuchungen.component';
import { AddschnelleinstiegComponent } from './addschnelleinstieg/addschnelleinstieg.component';
import { ADD_AUSGABE_ROUTE, ADD_EINNAHME_ROUTE, ADD_SCHNELLEINSTIEG_ROUTE, ADD_GEMEINSAME_BUCHUNG_ROUTE, ALLE_EINZELBUCHUNGEN_ROUTE, ALLE_GEMEINSAME_BUCHUNGEN_ROUTE, SETTINGS_ROUTE, ROOT_ROUTE } from './app-routes';


const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    canActivate: [AuthGuard], path: '', children:
      [
        { path: ADD_AUSGABE_ROUTE, component: AddausgabeComponent },
        { path: ADD_EINNAHME_ROUTE, component: AddeinnahmeComponent },
        { path: ADD_SCHNELLEINSTIEG_ROUTE, component: AddschnelleinstiegComponent },
        { path: ADD_GEMEINSAME_BUCHUNG_ROUTE, component: AddgemeinsameausgabeComponent },
        { path: ALLE_EINZELBUCHUNGEN_ROUTE, component: AllebuchungenComponent },
        { path: ALLE_GEMEINSAME_BUCHUNGEN_ROUTE, component: AllegemeinsamebuchungenComponent },
        { path: SETTINGS_ROUTE, component: SettingsComponent },
        { path: ROOT_ROUTE, component: AddschnelleinstiegComponent }
      ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }