import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppComponent }  from './app.component';
import { HomeComponent } from './component/home.component';
import { ReportFormComponent } from './forms/report-form.component';
import { ImageFormComponent } from './forms/image-form.component';

import { AppRoutingModule, routingComponents } from './app.routing';

@NgModule({
  imports:      [ BrowserModule, AppRoutingModule, FormsModule],
  declarations: [ AppComponent, routingComponents , HomeComponent, ReportFormComponent, ImageFormComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
