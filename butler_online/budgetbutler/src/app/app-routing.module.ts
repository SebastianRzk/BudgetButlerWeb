import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LoginComponent} from './auth/login/login.component';
import {AllebuchungenComponent} from './allebuchungen/allebuchungen.component';
import {SettingsComponent} from './settings/settings.component';
import {AllegemeinsamebuchungenComponent} from './allegemeinsamebuchungen/allegemeinsamebuchungen.component';
import {AddschnelleinstiegComponent} from './addschnelleinstieg/addschnelleinstieg.component';
import {
  ADD_SCHNELLEINSTIEG_ROUTE,
  ALLE_EINZELBUCHUNGEN_ROUTE,
  ALLE_GEMEINSAME_BUCHUNGEN_ROUTE,
  LOGIN_ROUTE,
  ROOT_ROUTE,
  SETTINGS_ROUTE
} from './app-routes';
import {AuthGuard} from './auth/auth.guard';


const routes: Routes = [
  {path: LOGIN_ROUTE, component: LoginComponent},

  {path: ADD_SCHNELLEINSTIEG_ROUTE, component: AddschnelleinstiegComponent, canActivate: [AuthGuard]},
  {path: ALLE_EINZELBUCHUNGEN_ROUTE, component: AllebuchungenComponent, canActivate: [AuthGuard]},
  {path: ALLE_GEMEINSAME_BUCHUNGEN_ROUTE, component: AllegemeinsamebuchungenComponent, canActivate: [AuthGuard]},
  {path: SETTINGS_ROUTE, component: SettingsComponent, canActivate: [AuthGuard]},
  {path: ROOT_ROUTE, component: AddschnelleinstiegComponent, canActivate: [AuthGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {})],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
