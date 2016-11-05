import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent }  from './app.component';
import { HomeComponent } from './component/home.component';
import { ReportFormComponent } from './forms/report-form.component';
import { MyIncidentFormComponent } from './forms/my-Incident-form.component';

import { AppRoutingModule, routingComponents } from './app.routing';
import { ReportService } from './_service/report.service';
import { AuthGuard } from './_guard/auth.guard';

@NgModule({
  imports:      [ BrowserModule, AppRoutingModule, FormsModule, HttpModule],
  declarations: [ AppComponent, routingComponents , HomeComponent,
                  ReportFormComponent, MyIncidentFormComponent ],
  providers: [ ReportService, AuthGuard ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
