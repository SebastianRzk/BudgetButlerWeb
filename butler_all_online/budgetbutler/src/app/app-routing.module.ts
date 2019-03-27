import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
 
import { AuthGuard } from './auth/auth.guard';
import { LoginComponent } from './auth/login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AddausgabeComponent } from './addausgabe/addausgabe.component';

 
const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { canActivate: [AuthGuard], path: '', children:
    [
      { path: 'dashboard', component: DashboardComponent},
      { path: 'addausgabe', component: AddausgabeComponent},
      { path: '', component: DashboardComponent}
    ]},
];
 
@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}