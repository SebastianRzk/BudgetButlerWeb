import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { provideHttpClient, withInterceptorsFromDi } from "@angular/common/http";
import { MatSidenav, MatSidenavContainer, MatSidenavModule } from "@angular/material/sidenav";
import { SidebarComponent } from "./pages/sidebar/sidebar/sidebar.component";
import { SidebarToggleComponent } from "./pages/sidebar/sidebar-toggle/sidebar-toggle.component";
import { RouterOutlet } from "@angular/router";
import { AsyncPipe } from "@angular/common";
import {MAT_DATE_LOCALE} from "@angular/material/core";

@NgModule({
  declarations: [
    AppComponent
  ],
  bootstrap: [AppComponent], imports: [BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSidenavModule,
    MatSidenavContainer,
    MatSidenav,
    SidebarComponent,
    SidebarToggleComponent,
    RouterOutlet,
    AsyncPipe
  ], providers: [provideHttpClient(withInterceptorsFromDi()),
    {provide: MAT_DATE_LOCALE, useValue: 'de-DE'},]
})
export class AppModule {
}
