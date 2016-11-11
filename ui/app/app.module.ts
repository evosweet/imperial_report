import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { enableProdMode } from '@angular/core';

import { AppComponent }  from './app.component';
import { HomeComponent } from './component/home.component';
import { ReportFormComponent } from './forms/report-form.component';
import { MyIncidentFormComponent } from './forms/my-Incident-form.component';
import { LoginFormComponent } from './forms/login-form.component';
import {  LoginComponent } from './component/login.component';
import { CreateComponent } from './component/admin/create.component';
import {  AboutComponent } from './component/admin/about.component';
import { EditComponent } from './component/admin/edit.component';

import { AppRoutingModule, routingComponents } from './app.routing';
import { ReportService } from './_service/report.service';
import { AuthGuard } from './_guard/auth.guard';
import {  AuthenticationService } from './_service/authentication.service';

enableProdMode()

@NgModule({
  imports:      [ BrowserModule, AppRoutingModule, FormsModule, HttpModule],
  declarations: [ AppComponent, routingComponents , HomeComponent,
                  ReportFormComponent, MyIncidentFormComponent, LoginFormComponent, 
                  LoginComponent, CreateComponent, AboutComponent, EditComponent ],
  providers: [ ReportService, AuthGuard, AuthenticationService ],
  bootstrap:    [ AppComponent ]
})
export class AppModule {
}
