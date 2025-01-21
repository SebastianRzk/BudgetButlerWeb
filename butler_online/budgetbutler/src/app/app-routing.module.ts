import {Routes} from '@angular/router';
import {LoginComponent} from './pages/auth/login/login.component';
import {AllebuchungenComponent} from './pages/allebuchungen/allebuchungen.component';
import {SettingsComponent} from './pages/settings/settings.component';
import {AllegemeinsamebuchungenComponent} from './pages/allegemeinsamebuchungen/allegemeinsamebuchungen.component';
import {AddBuchungComponent} from './pages/addbuchung/add-buchung.component';
import {
  ADD_DAUERAUFTRAG_ROUTE,
  ADD_SCHNELLEINSTIEG_ROUTE,
  ALLE_EINZELBUCHUNGEN_ROUTE,
  ALLE_GEMEINSAME_BUCHUNGEN_ROUTE,
  DAUERAUFTRAEGE_ROUTE,
  GEMEINSAME_DAUERAUFTRAEGE_ROUTE,
  KATEGORIEN_ROUTE,
  LOGIN_OFFLINE_ROUTE,
  LOGIN_ROUTE,
  LOGOUT_ROUTE,
  ROOT_ROUTE,
  SETTINGS_ROUTE
} from './app-routes';
import {canActivateAuthGuard} from './pages/auth/auth.guard';
import {LogoutComponent} from './pages/auth/logout/logout.component';
import {OfflineLoginComponent} from './pages/offline-login/offline-login.component';
import {AddDauerauftragComponent} from "./pages/adddauerauftrag/add-dauerauftrag.component";
import {DauerauftraegeComponent} from "./pages/dauerauftraege/dauerauftraege.component";
import {GemeinsameDauerauftraegeComponent} from "./pages/gemeinsame-dauerauftraege/gemeinsame-dauerauftraege.component";
import {KategorienComponent} from "./pages/kategorien/kategorien.component";


export const routes: Routes = [
  {path: LOGIN_ROUTE, component: LoginComponent},
  {path: LOGOUT_ROUTE, component: LogoutComponent},
  {path: LOGIN_OFFLINE_ROUTE, component: OfflineLoginComponent},

  {path: ADD_SCHNELLEINSTIEG_ROUTE, component: AddBuchungComponent, canActivate: [canActivateAuthGuard]},
  {path: ADD_DAUERAUFTRAG_ROUTE, component: AddDauerauftragComponent, canActivate: [canActivateAuthGuard]},
  {path: DAUERAUFTRAEGE_ROUTE, component: DauerauftraegeComponent, canActivate: [canActivateAuthGuard]},
  {path: GEMEINSAME_DAUERAUFTRAEGE_ROUTE, component: GemeinsameDauerauftraegeComponent, canActivate: [canActivateAuthGuard]},
  {path: ALLE_EINZELBUCHUNGEN_ROUTE, component: AllebuchungenComponent, canActivate: [canActivateAuthGuard]},
  {path: ALLE_GEMEINSAME_BUCHUNGEN_ROUTE, component: AllegemeinsamebuchungenComponent, canActivate: [canActivateAuthGuard]},
  {path: KATEGORIEN_ROUTE, component: KategorienComponent, canActivate: [canActivateAuthGuard]},
  {path: SETTINGS_ROUTE, component: SettingsComponent, canActivate: [canActivateAuthGuard]},
  {path: ROOT_ROUTE, component: AddBuchungComponent, canActivate: [canActivateAuthGuard]}
];
