import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent }  from './app.component';
import { HomeComponent } from './component/home.component';

import { AppRoutingModule, routingComponents } from './app.routing';

@NgModule({
  imports:      [ BrowserModule, AppRoutingModule],
  declarations: [ AppComponent, routingComponents , HomeComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
